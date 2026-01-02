'use client';

import React, { useRef, useState } from 'react';
import { ProTable, ActionType, ProColumns } from '@ant-design/pro-components';
import { Button, App, Popconfirm, Space, Modal, Form, Input, Select, Upload, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, UploadOutlined, ExportOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';

interface QuestionItem {
  id: number;
  question: string;
  answer: string;
  type: string;
  options?: string;
  created_at: string;
}

export default function QuestionsPage() {
  const actionRef = useRef<ActionType>();
  const { message: antMessage } = App.useApp();
  const [editModalVisible, setEditModalVisible] = useState(false);
  const [editingRecord, setEditingRecord] = useState<QuestionItem | null>(null);
  const [form] = Form.useForm();

  const columns: ProColumns<QuestionItem>[] = [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 80,
      search: false,
    },
    {
      title: '题目',
      dataIndex: 'question',
      copyable: true,
      ellipsis: true,
    },
    {
      title: '类型',
      dataIndex: 'type',
      width: 100,
      valueType: 'select',
      valueEnum: {
        'single': { text: '单选题' },
        'multiple': { text: '多选题' },
        'judgement': { text: '判断题' },
        'fill': { text: '填空题' },
        'essay': { text: '简答题' },
      },
    },
    {
      title: '答案',
      dataIndex: 'answer',
      search: false,
      ellipsis: true,
      width: 200,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      valueType: 'dateTime',
      search: false,
      width: 160,
    },
    {
      title: '操作',
      valueType: 'option',
      key: 'option',
      width: 120,
      render: (text, record, _, action) => [
        <a key="edit" onClick={() => handleEdit(record)}>
          编辑
        </a>,
        <Popconfirm
          key="delete"
          title="确定删除吗？"
          onConfirm={async () => {
            try {
              const res = await fetch(`/api/v1/admin/questions/${record.id}`, {
                method: 'DELETE',
              });
              if (res.ok) {
                antMessage.success('删除成功');
                action?.reload();
              } else {
                antMessage.error('删除失败');
              }
            } catch (e) {
              antMessage.error('请求失败');
            }
          }}
        >
          <a style={{ color: '#ff4d4f' }}>删除</a>
        </Popconfirm>,
      ],
    },
  ];

  const handleEdit = (record: QuestionItem) => {
    setEditingRecord(record);
    form.setFieldsValue({
      question: record.question,
      answer: record.answer,
      options: record.options || '',
      type: record.type || '',
    });
    setEditModalVisible(true);
  };

  const handleAdd = () => {
    setEditingRecord(null);
    form.resetFields();
    setEditModalVisible(true);
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();

      if (editingRecord) {
        // 更新
        const res = await fetch(`/api/v1/admin/questions/${editingRecord.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(values),
        });

        if (res.ok) {
          antMessage.success('更新成功');
          setEditModalVisible(false);
          actionRef.current?.reload();
        } else {
          antMessage.error('更新失败');
        }
      } else {
        // 新建
        const res = await fetch('/api/v1/admin/questions/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(values),
        });

        if (res.ok) {
          antMessage.success('创建成功');
          setEditModalVisible(false);
          actionRef.current?.reload();
        } else {
          antMessage.error('创建失败');
        }
      }
    } catch (e) {
      console.error('表单验证失败:', e);
    }
  };

  const uploadProps: UploadProps = {
    name: 'file',
    action: '/api/v1/admin/questions/import',
    accept: '.xlsx,.xls,.csv,.json',
    showUploadList: false,
    onChange(info) {
      if (info.file.status === 'done') {
        const result = info.file.response;
        if (result.success_count > 0) {
          antMessage.success(`导入成功！成功: ${result.success_count} 条${result.error_count > 0 ? `，失败: ${result.error_count} 条` : ''}`);
          actionRef.current?.reload();
        } else {
          antMessage.error('导入失败：' + (result.errors?.join(', ') || '未知错误'));
        }
      } else if (info.file.status === 'error') {
        antMessage.error('导入失败');
      }
    },
  };

  const handleExport = async (format: string) => {
    try {
      const res = await fetch(`/api/v1/admin/questions/export?format=${format}`);
      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `questions_export.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        antMessage.success('导出成功');
      } else {
        antMessage.error('导出失败');
      }
    } catch (e) {
      antMessage.error('导出失败');
    }
  };

  return (
    <>
      <ProTable<QuestionItem>
        headerTitle="题库列表"
        actionRef={actionRef}
        rowKey="id"
        search={{
          labelWidth: 'auto',
        }}
        toolBarRender={() => [
          <Button
            key="import"
            icon={<UploadOutlined />}
          >
            <Upload {...uploadProps}>
              <span>批量导入</span>
            </Upload>
          </Button>,
          <Space.Compact key="export">
            <Button
              icon={<ExportOutlined />}
              onClick={() => handleExport('xlsx')}
            >
              导出Excel
            </Button>
            <Button
              icon={<ExportOutlined />}
              onClick={() => handleExport('csv')}
            >
              导出CSV
            </Button>
            <Button
              icon={<ExportOutlined />}
              onClick={() => handleExport('json')}
            >
              导出JSON
            </Button>
          </Space.Compact>,
          <Button
            key="button"
            icon={<PlusOutlined />}
            onClick={handleAdd}
            type="primary"
          >
            新建题目
          </Button>,
        ]}
        request={async (params, sort, filter) => {
          const { current, pageSize, question, type } = params;
          const queryParams = new URLSearchParams({
            page: String(current),
            page_size: String(pageSize),
          });
          if (question) queryParams.append('keyword', question);
          if (type) queryParams.append('question_type', type);

          try {
            const res = await fetch(`/api/v1/admin/questions/?${queryParams.toString()}`);
            const data = await res.json();
            return {
              data: data.items,
              success: true,
              total: data.total,
            };
          } catch (e) {
            antMessage.error('获取数据失败');
            return {
              success: false,
            };
          }
        }}
        columns={columns}
        pagination={{
          pageSize: 10,
        }}
      />

      <Modal
        title={editingRecord ? '编辑题目' : '新建题目'}
        open={editModalVisible}
        onOk={handleSubmit}
        onCancel={() => setEditModalVisible(false)}
        width={600}
        okText="确定"
        cancelText="取消"
      >
        <Form
          form={form}
          layout="vertical"
          autoComplete="off"
        >
          <Form.Item
            label="题目类型"
            name="type"
            rules={[{ required: true, message: '请选择题目类型' }]}
          >
            <Select placeholder="请选择题目类型">
              <Select.Option value="single">单选题</Select.Option>
              <Select.Option value="multiple">多选题</Select.Option>
              <Select.Option value="judgement">判断题</Select.Option>
              <Select.Option value="fill">填空题</Select.Option>
              <Select.Option value="essay">简答题</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="题目内容"
            name="question"
            rules={[{ required: true, message: '请输入题目内容' }]}
          >
            <Input.TextArea rows={3} placeholder="请输入题目内容" />
          </Form.Item>

          <Form.Item
            label="选项（选填，单行表示一个选项）"
            name="options"
          >
            <Input.TextArea rows={4} placeholder="请输入选项，每行一个选项" />
          </Form.Item>

          <Form.Item
            label="答案"
            name="answer"
            rules={[{ required: true, message: '请输入答案' }]}
            extra="多个答案用 ### 分隔"
          >
            <Input.TextArea rows={2} placeholder="请输入答案，多个答案用 ### 分隔" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}
