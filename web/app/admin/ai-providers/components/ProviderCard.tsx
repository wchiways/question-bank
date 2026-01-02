'use client';

import React from 'react';
import { Card, Tag, Space, Button, Switch, Row, Col, Typography, Popconfirm } from 'antd';
import {
  ApiOutlined,
  EditOutlined,
  ThunderboltOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  WarningOutlined,
  DeleteOutlined,
} from '@ant-design/icons';

const { Text } = Typography;

interface Props {
  provider: any;
  providerKey: string;
  isDefault: boolean;
  isTesting: boolean;
  onTest: () => void;
  onEdit: () => void;
  onToggle: (checked: boolean) => void;
  onSetDefault: () => void;
  onDelete: () => void;
}

export const ProviderCard: React.FC<Props> = ({
  provider,
  providerKey,
  isDefault,
  isTesting,
  onTest,
  onEdit,
  onToggle,
  onSetDefault,
  onDelete,
}) => {
  const getProviderIcon = (key: string, name: string) => {
    // 定义关键词到emoji的映射
    const keywordEmojis: Record<string, string> = {
      // AI/智能相关
      'open': '🤖',
      'openai': '🤖',
      'claude': '🧠',
      'anthropic': '🧠',
      'gemini': '✨',
      'gpt': '💬',
      'ai': '🤖',
      '智能': '🧠',

      // 云服务相关
      'cloud': '☁️',
      '云': '☁️',
      'ali': '🟠',
      'aliyun': '🟠',
      'ali_bailian': '🟠',
      'bailian': '🟠',
      'tencent': '🟢',
      'huawei': '🔴',
      'baidu': '🔵',

      // 搜索/数据相关
      'google': '🔍',
      'search': '🔍',
      'data': '📊',
      '数据库': '🗄️',

      // 火焰/性能相关
      'fire': '🔥',
      'volcengine': '🔥',
      'volcano': '🔥',
      '火山': '🔥',
      'speed': '⚡',

      // 珠宝/品质相关
      'silicon': '💎',
      'siliconflow': '💎',
      'flow': '💧',
      'stream': '💧',

      // 智谱相关
      'zhipu': '🎯',
      'chatglm': '💬',
      'glm': '💬',
      '智谱': '🎯',

      // 其他常见服务商
      'azure': '🔷',
      'microsoft': '🪟',
      'aws': '🟠',
      'amazon': '📦',
      'meta': '🔵',
      'facebook': '🔵',
      'twitter': '🐦',
      'x': '❌',

      // 通用图标
      'api': '🔌',
      'service': '⚙️',
      'provider': '🏢',
    };

    // 1. 优先匹配完整的 key
    if (keywordEmojis[key]) {
      return keywordEmojis[key];
    }

    // 2. 将 key 和 name 转为小写，方便匹配
    const keyLower = key.toLowerCase();
    const nameLower = name.toLowerCase();

    // 3. 尝试匹配 key 中的关键词
    for (const [keyword, emoji] of Object.entries(keywordEmojis)) {
      if (keyLower.includes(keyword)) {
        return emoji;
      }
    }

    // 4. 尝试匹配 name 中的关键词
    for (const [keyword, emoji] of Object.entries(keywordEmojis)) {
      if (nameLower.includes(keyword)) {
        return emoji;
      }
    }

    // 5. 都匹配不到，使用通用图标
    return '⚙️';
  };

  const getStatusTags = () => {
    const tags = [];

    if (isDefault) {
      tags.push(<Tag color="blue" key="default">默认</Tag>);
    }

    if (provider.enabled) {
      tags.push(<Tag color="green" key="enabled">已启用</Tag>);
    } else {
      tags.push(<Tag color="red" key="disabled">未启用</Tag>);
    }

    if (!provider.api_key || provider.api_key.includes('****') || provider.api_key === '未配置') {
      tags.push(<Tag color="orange" key="unconfigured">未配置</Tag>);
    }

    return tags;
  };

  return (
    <Card
      style={{ marginBottom: 16 }}
      extra={
        <Space size="small">
          <Button
            icon={<ApiOutlined />}
            onClick={onTest}
            disabled={!provider.enabled || isTesting}
            loading={isTesting}
          >
            测试连接
          </Button>
          <Button icon={<EditOutlined />} onClick={onEdit}>
            编辑
          </Button>
          {!isDefault && (
            <Button
              type="link"
              onClick={onSetDefault}
              disabled={!provider.enabled}
            >
              设为默认
            </Button>
          )}
          <Popconfirm
            title="确定要删除这个服务商吗？"
            description="删除后将无法恢复"
            onConfirm={onDelete}
            okText="确定"
            cancelText="取消"
          >
            <Button
              danger
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
          <Switch
            checked={provider.enabled}
            onChange={onToggle}
            checkedChildren="启用"
            unCheckedChildren="禁用"
          />
        </Space>
      }
    >
      <Row gutter={16}>
        <Col span={24}>
          <Space direction="vertical" size="small" style={{ width: '100%' }}>
            <div>
              <Text strong style={{ fontSize: 16 }}>
                {getProviderIcon(providerKey, provider.name)} {provider.name}
              </Text>
              {getStatusTags()}
            </div>

            <div>
              <Text type="secondary">API Key: </Text>
              <Text code>{provider.api_key}</Text>
            </div>

            <Row gutter={16}>
              <Col span={8}>
                <Text type="secondary">Model: </Text>
                <Text>{provider.model}</Text>
              </Col>
              <Col span={8}>
                <Text type="secondary">Max Tokens: </Text>
                <Text>{provider.max_tokens}</Text>
              </Col>
              <Col span={8}>
                <Text type="secondary">Temperature: </Text>
                <Text>{provider.temperature}</Text>
              </Col>
            </Row>
          </Space>
        </Col>
      </Row>
    </Card>
  );
};
