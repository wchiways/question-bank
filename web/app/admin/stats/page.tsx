'use client';

import React, { useEffect, useState, useRef } from 'react';
import { PageContainer, StatisticCard } from '@ant-design/pro-components';
import { Row, Col, App, Card, Progress, Table, Tag, Space } from 'antd';
import {
  PieChartOutlined,
  UserOutlined,
  FileTextOutlined,
  CloudServerOutlined,
  DatabaseOutlined,
  CheckCircleOutlined,
  LineChartOutlined,
  BarChartOutlined
} from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts/core';

const { Statistic } = StatisticCard;

interface StatsData {
  questions_total: number;
  log_size_bytes: number;
  ai_provider: string;
  debug_mode: boolean;
}

interface QuestionTypeStat {
  type: string;
  count: number;
  percent: number;
}

export default function StatsPage() {
  const [data, setData] = useState<StatsData>({
    questions_total: 0,
    log_size_bytes: 0,
    ai_provider: '-',
    debug_mode: false
  });
  const [questionTypes, setQuestionTypes] = useState<QuestionTypeStat[]>([]);
  const [loading, setLoading] = useState(true);
  const { message } = App.useApp();

  useEffect(() => {
    loadStats();
    loadQuestionTypes();
  }, []);

  const loadStats = async () => {
    try {
      const res = await fetch('/api/v1/admin/stats/');
      const jsonData = await res.json();
      setData(jsonData);
    } catch (e) {
      message.error('获取统计失败');
    } finally {
      setLoading(false);
    }
  };

  const loadQuestionTypes = async () => {
    try {
      // 使用 URLSearchParams 构建查询参数，避免解析问题
      const params = new URLSearchParams({
        page: '1',
        page_size: '10000'
      });
      const res = await fetch(`/api/v1/admin/questions/?${params.toString()}`);
      const jsonData = await res.json();

      if (!jsonData.items || !Array.isArray(jsonData.items)) {
        console.warn('API返回数据格式异常:', jsonData);
        setQuestionTypes([]);
        return;
      }

      const typeMap: Record<string, number> = {};
      jsonData.items.forEach((item: any) => {
        const type = item.type || 'unknown';
        typeMap[type] = (typeMap[type] || 0) + 1;
      });

      const total = jsonData.items.length || 0;
      const typeStats: QuestionTypeStat[] = Object.entries(typeMap).map(([type, count]) => ({
        type,
        count,
        percent: total > 0 ? Math.round((count / total) * 100) : 0
      }));

      console.log('题目类型统计:', typeStats); // 添加调试日志
      setQuestionTypes(typeStats);
    } catch (e) {
      console.error('获取题目类型统计失败:', e);
      setQuestionTypes([]);
    }
  };

  // 题目类型饼图配置 - 简洁风格
  const getPieChartOption = () => {
    const typeMap: Record<string, string> = {
      single: '单选题',
      multiple: '多选题',
      judgement: '判断题',
      fill: '填空题',
      essay: '简答题',
    };

    // 简洁的配色方案
    const colorPalette = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'];

    return {
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        textStyle: {
          fontSize: 12
        }
      },
      series: [
        {
          name: '题目类型',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['35%', '50%'],
          avoidLabelOverlap: true,
          itemStyle: {
            borderRadius: 8,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}: {d}%',
            fontSize: 12
          },
          labelLine: {
            show: true,
            length: 15,
            length2: 10,
            smooth: true
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 14,
              fontWeight: 'bold'
            }
          },
          data: questionTypes.map((item, index) => ({
            value: item.count,
            name: typeMap[item.type] || item.type,
            itemStyle: {
              color: colorPalette[index % colorPalette.length]
            }
          }))
        }
      ]
    };
  };

  // 题目类型柱状图配置 - 简洁风格
  const getBarChartOption = () => {
    const typeMap: Record<string, string> = {
      single: '单选题',
      multiple: '多选题',
      judgement: '判断题',
      fill: '填空题',
      essay: '简答题',
    };

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: questionTypes.map(item => typeMap[item.type] || item.type),
        axisLabel: {
          interval: 0,
          rotate: 0,
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#ddd'
          }
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          fontSize: 12
        },
        axisLine: {
          show: false
        },
        splitLine: {
          lineStyle: {
            color: '#f0f0f0',
            type: 'dashed'
          }
        }
      },
      series: [
        {
          name: '题目数量',
          type: 'bar',
          barWidth: '50%',
          data: questionTypes.map((item, index) => ({
            value: item.count,
            itemStyle: {
              color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'][index % 5],
              borderRadius: [4, 4, 0, 0]
            }
          })),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.2)'
            }
          }
        }
      ]
    };
  };

  // 系统指标雷达图配置 - 简洁风格
  const getRadarChartOption = () => {
    const questionScore = Math.min(data.questions_total / 100, 1) * 100;
    const logScore = Math.max(100 - (data.log_size_bytes / 1024 / 1024) * 10, 50);
    const aiScore = data.ai_provider ? 90 : 0;

    return {
      tooltip: {},
      radar: {
        indicator: [
          { name: '题库完整性', max: 100 },
          { name: '系统健康度', max: 100 },
          { name: 'AI服务', max: 100 },
          { name: '日志规范', max: 100 },
          { name: '缓存效率', max: 100 }
        ],
        radius: 60,
        splitNumber: 4,
        axisName: {
          color: '#666',
          fontSize: 12
        },
        splitArea: {
          show: true,
          areaStyle: {
            color: ['rgba(114, 172, 209, 0.1)', 'rgba(114, 172, 209, 0.2)']
          }
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(114, 172, 209, 0.3)'
          }
        },
        axisLine: {
          lineStyle: {
            color: 'rgba(114, 172, 209, 0.3)'
          }
        }
      },
      series: [
        {
          name: '系统指标',
          type: 'radar',
          data: [
            {
              value: [questionScore, 90, aiScore, logScore, 85],
              name: '当前状态',
              areaStyle: {
                color: 'rgba(84, 112, 198, 0.3)'
              },
              lineStyle: {
                color: '#5470c6',
                width: 2
              },
              itemStyle: {
                color: '#5470c6'
              }
            }
          ]
        }
      ]
    };
  };

  const typeColumns = [
    {
      title: '题目类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          single: { text: '单选题', color: 'blue' },
          multiple: { text: '多选题', color: 'green' },
          judgement: { text: '判断题', color: 'orange' },
          fill: { text: '填空题', color: 'purple' },
          essay: { text: '简答题', color: 'cyan' },
        };
        const info = typeMap[type] || { text: type, color: 'default' };
        return <Tag color={info.color}>{info.text}</Tag>;
      }
    },
    {
      title: '数量',
      dataIndex: 'count',
      key: 'count',
    },
    {
      title: '占比',
      dataIndex: 'percent',
      key: 'percent',
      render: (percent: number) => (
        <Progress
          percent={percent}
          size="small"
          status={percent < 20 ? 'exception' : undefined}
        />
      ),
    },
  ];

  return (
    <PageContainer loading={loading}>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* 核心统计卡片 */}
        <Row gutter={[16, 16]}>
          <Col span={8}>
            <StatisticCard
              statistic={{
                title: '总题目数',
                value: data.questions_total || 0,
                icon: <PieChartOutlined style={{ fontSize: 24, color: '#1890ff' }} />,
                description: '题库总量',
              }}
            />
          </Col>
          <Col span={8}>
            <StatisticCard
              statistic={{
                title: '日志文件',
                value: data.log_size_bytes ? (data.log_size_bytes / 1024).toFixed(2) : '0',
                suffix: 'KB',
                icon: <FileTextOutlined style={{ fontSize: 24, color: '#faad14' }} />,
                description: '日志大小',
              }}
            />
          </Col>
          <Col span={8}>
            <StatisticCard
              statistic={{
                title: 'AI提供商',
                value: data.ai_provider || '-',
                icon: <CloudServerOutlined style={{ fontSize: 24, color: '#722ed1' }} />,
                description: '当前使用',
              }}
            />
          </Col>
        </Row>

        {/* 图表展示区域 */}
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Card
              title={<><PieChartOutlined /> 题目类型分布（饼图）</>}
              extra={<Tag color={data.debug_mode ? 'red' : 'green'}>{data.debug_mode ? '调试模式' : '生产模式'}</Tag>}
            >
              {questionTypes.length > 0 ? (
                <ReactECharts
                  option={getPieChartOption()}
                  style={{ height: '350px' }}
                  notMerge={true}
                  lazyUpdate={true}
                />
              ) : (
                <div style={{ textAlign: 'center', padding: '100px 0', color: '#999' }}>
                  暂无数据
                </div>
              )}
            </Card>
          </Col>

          <Col span={12}>
            <Card title={<><BarChartOutlined /> 题目类型统计（柱状图）</>}>
              {questionTypes.length > 0 ? (
                <ReactECharts
                  option={getBarChartOption()}
                  style={{ height: '350px' }}
                  notMerge={true}
                  lazyUpdate={true}
                />
              ) : (
                <div style={{ textAlign: 'center', padding: '100px 0', color: '#999' }}>
                  暂无数据
                </div>
              )}
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Card title={<><CheckCircleOutlined /> 系统健康度评估（雷达图）</>}>
              <ReactECharts
                option={getRadarChartOption()}
                style={{ height: '350px' }}
                notMerge={true}
                lazyUpdate={true}
              />
            </Card>
          </Col>

          <Col span={12}>
            <Card title={<><DatabaseOutlined /> 题目类型详情</>}>
              <Table
                dataSource={questionTypes}
                columns={typeColumns}
                rowKey="type"
                pagination={false}
                size="small"
              />
            </Card>
          </Col>
        </Row>

        {/* 系统状态卡片 */}
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Card title={<><CheckCircleOutlined /> 系统状态详情</>}>
              <Row gutter={[16, 16]}>
                <Col span={12}>
                  <StatisticCard
                    statistic={{
                      title: '题库健康度',
                      value: data.questions_total > 100 ? 100 : data.questions_total,
                      suffix: '/ 100',
                    }}
                    footer={
                      <Progress
                        percent={data.questions_total > 100 ? 100 : data.questions_total}
                        status={data.questions_total > 50 ? 'success' : 'exception'}
                      />
                    }
                  />
                </Col>
                <Col span={12}>
                  <StatisticCard
                    statistic={{
                      title: '用户活跃度',
                      value: data.users_total > 10 ? 100 : data.users_total * 10,
                      suffix: '/ 100',
                    }}
                    footer={
                      <Progress
                        percent={data.users_total > 10 ? 100 : data.users_total * 10}
                        status={data.users_total > 5 ? 'success' : 'exception'}
                      />
                    }
                  />
                </Col>
              </Row>
            </Card>
          </Col>

          <Col span={12}>
            <Card title="系统信息">
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <strong>题目总量：</strong>{data.questions_total} 题
                </div>
                <div>
                  <strong>用户总数：</strong>{data.users_total} 人
                </div>
                <div>
                  <strong>AI提供商：</strong>{data.ai_provider || '未配置'}
                </div>
                <div>
                  <strong>运行模式：</strong>
                  <Tag color={data.debug_mode ? 'red' : 'green'}>
                    {data.debug_mode ? '调试模式' : '生产模式'}
                  </Tag>
                </div>
                <div>
                  <strong>日志大小：</strong>
                  {(data.log_size_bytes / 1024).toFixed(2)} KB
                </div>
              </Space>
            </Card>
          </Col>
        </Row>
      </Space>
    </PageContainer>
  );
}
