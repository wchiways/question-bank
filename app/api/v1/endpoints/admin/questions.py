from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from io import BytesIO
import pandas as pd
from app.api import deps
from app.repositories.question_repository import QuestionRepository
from app.models.question import QuestionRead, QuestionCreate, QuestionUpdate

router = APIRouter()

@router.get("/", response_model=dict)
async def get_questions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=10000, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    question_type: Optional[str] = Query(None, description="题目类型"),
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """
    获取题目列表，支持分页和搜索

    Args:
        page: 页码（从1开始）
        page_size: 每页数量（最大10000，用于统计分析）
        keyword: 可选的搜索关键词
        question_type: 可选的题目类型筛选
        question_repo: Question仓储实例

    Returns:
        包含items、total、page、page_size的字典
    """
    skip = (page - 1) * page_size

    # 使用 Repository 的分页方法（遵循单一职责原则！）
    return await question_repo.get_paginated(
        skip=skip,
        limit=page_size,
        keyword=keyword,
        question_type=question_type
    )

@router.post("/import")
async def import_questions(
    file: UploadFile = File(...),
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """
    批量导入题目 (支持 Excel, CSV, JSON)

    Args:
        file: 上传的文件
        question_repo: Question仓储实例

    Returns:
        导入结果统计
    """
    try:
        content = await file.read()

        if not content:
            raise HTTPException(status_code=400, detail="File is empty")

        # 根据文件扩展名判断格式
        filename = file.filename or ""
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            import io
            df = pd.read_excel(io.BytesIO(content))
        elif filename.endswith(".csv"):
            import io
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith(".json"):
            import json
            data = json.loads(content.decode("utf-8"))
            df = pd.DataFrame(data)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # 统计结果
        success_count = 0
        error_count = 0

        for _, row in df.iterrows():
            try:
                # 智能列名映射
                question = None
                answer = None
                options = None
                question_type = None

                # 查找题目列
                for col in ["题目", "question", "Question", "title"]:
                    if col in df.columns:
                        question = row[col]
                        break

                # 查找答案列
                for col in ["答案", "answer", "Answer"]:
                    if col in df.columns:
                        answer = row[col]
                        break

                # 查找选项列
                for col in ["选项", "options", "Options"]:
                    if col in df.columns:
                        options = row[col]
                        break

                # 查找类型列
                for col in ["类型", "type", "Type"]:
                    if col in df.columns:
                        question_type = row[col]
                        break

                if not question or not answer:
                    error_count += 1
                    continue

                await question_repo.create_question(
                    question=str(question),
                    answer=str(answer),
                    options=str(options) if options else None,
                    question_type=str(question_type) if question_type else None
                )
                success_count += 1

            except Exception:
                error_count += 1

        return {
            "message": f"导入完成！成功: {success_count}, 失败: {error_count}",
            "success": success_count,
            "errors": error_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.get("/export")
async def export_questions(
    format: str = Query("xlsx"),
    keyword: Optional[str] = Query(None),
    question_type: Optional[str] = Query(None),
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """
    批量导出题目 (支持 Excel, CSV, JSON)

    Args:
        format: 导出格式
        keyword: 可选的关键词筛选
        question_type: 可选的类型筛选
        question_repo: Question仓储实例

    Returns:
        文件下载响应
    """
    try:
        # 获取数据
        result = await question_repo.get_paginated(
            skip=0,
            limit=10000,  # 最大导出10000条
            keyword=keyword,
            question_type=question_type
        )

        items = result["items"]

        if not items:
            raise HTTPException(status_code=404, detail="No questions found")

        # 转换为字典列表
        data = []
        for item in items:
            data.append({
                "ID": item.id,
                "题目": item.question,
                "答案": item.answer,
                "选项": item.options or "",
                "类型": item.type or "",
                "创建时间": item.created_at.strftime("%Y-%m-%d %H:%M:%S") if item.created_at else ""
            })

        df = pd.DataFrame(data)

        # 根据格式返回
        if format == "csv":
            output = BytesIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)

            return StreamingResponse(
                output,
                media_type="text/csv",
                headers={
                    "Content-Disposition": "attachment; filename=questions_export.csv"
                }
            )

        elif format == "json":
            import json
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            output = BytesIO(json_data.encode('utf-8'))

            return StreamingResponse(
                BytesIO(json_data.encode('utf-8')),
                media_type="application/json",
                headers={
                    "Content-Disposition": "attachment; filename=questions_export.json"
                }
            )

        else:  # xlsx (default)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='题目')
            output.seek(0)

            return StreamingResponse(
                output,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={
                    "Content-Disposition": "attachment; filename=questions_export.xlsx"
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(
    question_id: int,
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """获取单个题目详情"""
    question = await question_repo.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("/", response_model=QuestionRead)
async def create_question(
    question_in: QuestionCreate,
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """创建题目"""
    return await question_repo.create_question(
        question=question_in.question,
        answer=question_in.answer,
        options=question_in.options or "",
        question_type=question_in.type or ""
    )

@router.put("/{question_id}", response_model=QuestionRead)
async def update_question(
    question_id: int,
    question_in: QuestionUpdate,
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """更新题目"""
    question = await question_repo.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    update_data = question_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(question, key, value)
    
    return await question_repo.update(question)

@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """删除题目"""
    success = await question_repo.delete(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}


