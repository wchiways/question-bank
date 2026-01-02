'use client';

import React, { useEffect, useState } from 'react';
import { PageContainer, ProCard, StatisticCard } from '@ant-design/pro-components';
import { Row, Col, Card, App, Typography, Space, Divider, Timeline } from 'antd';
import {
  BookOutlined,
  MessageOutlined,
  ClockCircleOutlined,
  RocketOutlined,
  SafetyOutlined,
  ThunderboltOutlined,
  DatabaseOutlined
} from '@ant-design/icons';

const { Statistic } = StatisticCard;
const { Title, Text, Paragraph } = Typography;

interface SystemStats {
  questions_total: number;
  log_size_bytes: number;
  ai_provider: string;
  debug_mode: boolean;
}

export default function AdminHome() {
  const [stats, setStats] = useState<SystemStats>({
    questions_total: 0,
    log_size_bytes: 0,
    ai_provider: '-',
    debug_mode: false
  });
  const [loading, setLoading] = useState(true);
  const { message } = App.useApp();

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const res = await fetch('/api/v1/admin/stats/');
      const data = await res.json();
      setStats(data);
    } catch (e) {
      message.error('获取统计数据失败');
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: '题库管理',
      description: '管理题目、批量导入导出',
      icon: <BookOutlined style={{ fontSize: 32, color: '#1890ff' }} />,
      link: '/admin/questions',
    },
    {
      title: '统计分析',
      description: '查看系统使用情况',
      icon: <MessageOutlined style={{ fontSize: 32, color: '#722ed1' }} />,
      link: '/admin/stats',
    },
    {
      title: '系统配置',
      description: '管理系统配置和参数',
      icon: <SafetyOutlined style={{ fontSize: 32, color: '#faad14' }} />,
      link: '/admin/config',
    },
  ];

  const systemFeatures = [
    '✨ FastAPI + AsyncIO 高性能异步架构',
    '🚀 SQLModel 数据库 ORM',
    '🤖 多 AI 提供商支持 (OpenAI/DeepSeek/Volcengine)',
    '📊 完善的管理后台系统',
    '📝 结构化日志和监控',
    '💾 Redis 缓存支持',
  ];

  return (
    <PageContainer loading={loading}>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* 欢迎区域 */}
        <Card>
          <Space direction="vertical" size="small">
            <Title level={2} style={{ margin: 0 }}>
              <RocketOutlined /> 欢迎使用 OCS-TIKU 管理后台
            </Title>
            <Paragraph type="secondary">
              本系统是基于 FastAPI + Next.js 构建的高性能题库管理系统，提供完整的题目管理、统计分析和系统配置功能。
            </Paragraph>
          </Space>
        </Card>

        {/* 核心统计数据 */}
        <Row gutter={[16, 16]}>
          <Col span={8}>
            <StatisticCard
              statistic={{
                title: '总题目数',
                value: stats.questions_total || 0,
                icon: <BookOutlined style={{ fontSize: 24, color: '#1890ff' }} />,
                description: '题库总量',
              }}
            />
          </Col>
          <Col span={8}>
            <StatisticCard
              statistic={{
                title: '日志大小',
                value: stats.log_size_bytes ? (stats.log_size_bytes / 1024).toFixed(2) : '0',
                suffix: 'KB',
                icon: <MessageOutlined style={{ fontSize: 24, color: '#722ed1' }} />,
                description: '系统日志',
              }}
            />
          </Col>
          <Col span={8}>
            <StatisticCard
              statistic={{
                title: 'AI提供商',
                value: stats.ai_provider || '-',
                icon: <ThunderboltOutlined style={{ fontSize: 24, color: '#faad14' }} />,
                description: '当前使用',
              }}
            />
          </Col>
        </Row>

        {/* 快捷入口 */}
        <ProCard title="快捷入口" headerBordered>
          <Row gutter={[16, 16]}>
            {quickActions.map((action) => (
              <Col span={8} key={action.title}>
                <Card
                  hoverable
                  onClick={() => (window.location.href = action.link)}
                  style={{ textAlign: 'center', height: '100%' }}
                >
                  <Space direction="vertical" size="middle">
                    {action.icon}
                    <div>
                      <Title level={5} style={{ margin: 0 }}>
                        {action.title}
                      </Title>
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {action.description}
                      </Text>
                    </div>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        </ProCard>

        {/* 系统特性 */}
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Card title={<><DatabaseOutlined /> 系统特性</>}>
              <Space direction="vertical" size="small" style={{ width: '100%' }}>
                {systemFeatures.map((feature, index) => (
                  <div key={index} style={{ padding: '4px 0' }}>
                    {feature}
                  </div>
                ))}
              </Space>
            </Card>
          </Col>

          <Col span={12}>
            <Card title={<><ClockCircleOutlined /> 快速上手</>}>
              <Timeline
                items={[
                  {
                    children: (
                      <div>
                        <Text strong>题库管理</Text>
                        <br />
                        <Text type="secondary">批量导入导出题目，支持Excel/CSV/JSON格式</Text>
                      </div>
                    ),
                  },
                  {
                    children: (
                      <div>
                        <Text strong>统计分析</Text>
                        <br />
                        <Text type="secondary">查看统计数据、题目分布、系统状态</Text>
                      </div>
                    ),
                  },
                  {
                    children: (
                      <div>
                        <Text strong>配置管理</Text>
                        <br />
                        <Text type="secondary">在线编辑配置、切换AI提供商</Text>
                      </div>
                    ),
                  },
                ]}
              />
            </Card>
          </Col>
        </Row>
      </Space>
    </PageContainer>
  );
}
