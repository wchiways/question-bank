'use client';

import React, { useState } from 'react';
import { PageContainer, ProCard } from '@ant-design/pro-components';
import { Button, Space, Spin, App, Typography, Divider } from 'antd';
import {
  ThunderboltOutlined,
  ReloadOutlined,
  RocketOutlined,
  PlusOutlined,
} from '@ant-design/icons';
import { useAIProviders } from './hooks/useAIProviders';
import { ProviderCard } from './components/ProviderCard';
import { ProviderFormModal } from './components/ProviderFormModal';
import { AddProviderModal } from './components/AddProviderModal';

const { Title, Text } = Typography;

export default function AIProvidersPage() {
  const { message } = App.useApp();

  const {
    config,
    loading,
    testing,
    reload,
    updateProvider,
    testProvider,
    setDefaultProvider,
    createProvider,
    deleteProvider,
  } = useAIProviders();

  const [editingProvider, setEditingProvider] = useState<any>(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [addModalVisible, setAddModalVisible] = useState(false);

  const handleEdit = (providerKey: string) => {
    const provider = config?.providers[providerKey];
    if (provider) {
      setEditingProvider({
        key: providerKey,
        ...provider,
      });
      setModalVisible(true);
    }
  };

  const handleSubmit = async (values: any) => {
    if (!editingProvider || !editingProvider.key) {
      message.error('无效的服务商');
      return false;
    }

    const success = await updateProvider(editingProvider.key, values);
    if (success) {
      message.success('配置更新成功');
      setModalVisible(false);
      setEditingProvider(null);
    } else {
      message.error('配置更新失败');
    }
    return success;
  };

  const handleTest = async (providerKey: string) => {
    const result = await testProvider(providerKey);

    if (result.success) {
      message.success(
        `✅ ${config?.providers[providerKey].name} 连接成功！响应时间: ${result.latency}ms`
      );
    } else {
      message.error(`❌ 连接失败: ${result.error}`);
    }
  };

  const handleSetDefault = async (providerKey: string) => {
    const success = await setDefaultProvider(providerKey);
    if (success) {
      message.success(`已设置 ${config?.providers[providerKey].name} 为默认提供商`);
    } else {
      message.error('设置失败');
    }
  };

  const handleToggle = async (providerKey: string, checked: boolean) => {
    const success = await updateProvider(providerKey, { enabled: checked });
    if (success) {
      message.success(
        checked
          ? `已启用 ${config?.providers[providerKey].name}`
          : `已禁用 ${config?.providers[providerKey].name}`
      );
    } else {
      message.error('操作失败');
    }
  };

  const handleAdd = async (values: any) => {
    const success = await createProvider(values);
    if (success) {
      message.success('服务商创建成功');
      setAddModalVisible(false);
    } else {
      message.error('服务商创建失败');
    }
    return success;
  };

  const handleDelete = async (providerKey: string) => {
    const success = await deleteProvider(providerKey);
    if (success) {
      message.success('服务商删除成功');
    } else {
      message.error('服务商删除失败');
    }
  };

  if (loading || !config) {
    return (
      <PageContainer>
        <div style={{ textAlign: 'center', padding: '100px 0' }}>
          <Spin size="large" />
        </div>
      </PageContainer>
    );
  }

  const providers = Object.entries(config.providers);

  return (
    <PageContainer
      title="AI 服务商配置"
      subTitle="管理和配置 AI 服务提供商，支持测试连接和动态切换"
    >
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* 全局设置 */}
        <ProCard title={<><RocketOutlined /> 全局设置</>}>
          <Space direction="vertical" size="small" style={{ width: '100%' }}>
            <Space size="large" wrap>
              <div>
                <Text type="secondary">默认提供商: </Text>
                <Text strong style={{ fontSize: 16 }}>
                  {config.providers[config.default_provider]?.name || '未设置'}
                </Text>
              </div>
              <Divider type="vertical" />
              <div>
                <Text type="secondary">超时时间: </Text>
                <Text strong>{config.timeout}s</Text>
              </div>
              <Divider type="vertical" />
              <div>
                <Text type="secondary">重试次数: </Text>
                <Text strong>{config.max_retries}</Text>
              </div>
              <Divider type="vertical" />
              <div>
                <Text type="secondary">已配置服务商: </Text>
                <Text strong>
                  {providers.filter(([_, p]) => p.enabled).length} / {providers.length}
                </Text>
              </div>
            </Space>
          </Space>
        </ProCard>

        {/* 服务商列表 */}
        <ProCard
          title={
            <>
              <ThunderboltOutlined /> 服务商列表 ({providers.length})
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => setAddModalVisible(true)}
                style={{ marginLeft: 16 }}
              >
                添加服务商
              </Button>
            </>
          }
          headerBordered
        >
          {providers.map(([key, provider]) => (
            <ProviderCard
              key={key}
              provider={provider}
              providerKey={key}
              isDefault={config.default_provider === key}
              isTesting={testing[key] || false}
              onEdit={() => handleEdit(key)}
              onTest={() => handleTest(key)}
              onToggle={(checked) => handleToggle(key, checked)}
              onSetDefault={() => handleSetDefault(key)}
              onDelete={() => handleDelete(key)}
            />
          ))}
        </ProCard>

        {/* 快速操作 */}
        <ProCard title="快速操作" headerBordered>
          <Space>
            <Button icon={<ReloadOutlined />} onClick={reload}>
              重新加载配置
            </Button>
          </Space>
        </ProCard>
      </Space>

      {/* 编辑模态框 */}
      <ProviderFormModal
        visible={modalVisible}
        provider={editingProvider}
        onSubmit={handleSubmit}
        onCancel={() => {
          setModalVisible(false);
          setEditingProvider(null);
        }}
      />

      {/* 添加服务商模态框 */}
      <AddProviderModal
        visible={addModalVisible}
        onSubmit={handleAdd}
        onCancel={() => setAddModalVisible(false)}
      />
    </PageContainer>
  );
}
