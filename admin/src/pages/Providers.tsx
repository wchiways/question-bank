import React, { useEffect, useState } from 'react';
import { Table, Button, Tag, Space, Card, Modal, Form, Input, InputNumber, Switch, message, Tooltip, Badge } from 'antd';
import { PlusOutlined, DeleteOutlined, StarOutlined, StarFilled, EditOutlined } from '@ant-design/icons';
import api from '../utils/api';

interface Provider {
  name: string;
  enabled: boolean;
  api_key: string;
  api_url: string;
  model: string;
  max_tokens: number;
  temperature: number;
}

const Providers: React.FC = () => {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [defaultProvider, setDefaultProvider] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProvider, setEditingProvider] = useState<string | null>(null);
  const [form] = Form.useForm();

  const fetchProviders = async () => {
    setLoading(true);
    try {
      const { data } = await api.get('/providers');
      setDefaultProvider(data.default);
      
      const list = Object.entries(data.providers).map(([key, val]: [string, any]) => ({
        name: key,
        ...val
      }));
      setProviders(list);
    } catch (error) {
      message.error('加载服务商失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProviders();
  }, []);

  const handleDelete = async (name: string) => {
    Modal.confirm({
      title: '确认删除？',
      content: `是否删除服务商 ${name}？`,
      okType: 'danger',
      onOk: async () => {
        try {
          await api.delete(`/providers/${name}`);
          message.success('服务商已删除');
          fetchProviders();
        } catch (error) {
          message.error('删除服务商失败');
        }
      }
    });
  };

  const handleSetDefault = async (name: string) => {
    try {
      await api.post('/providers/default', { name });
      message.success(`默认服务商已设为 ${name}`);
      fetchProviders();
    } catch (error) {
      message.error('设置默认服务商失败');
    }
  };

  const handleEdit = (record: Provider) => {
    setEditingProvider(record.name);
    form.setFieldsValue(record);
    setIsModalOpen(true);
  };

  const handleAdd = () => {
    setEditingProvider(null);
    form.resetFields();
    form.setFieldsValue({ enabled: true, max_tokens: 512, temperature: 0.1 });
    setIsModalOpen(true);
  };

  const handleSave = async (values: any) => {
    try {
      const payload = {
        name: values.name,
        config: values
      };
      await api.post('/providers', payload);
      message.success('服务商已保存');
      setIsModalOpen(false);
      form.resetFields();
      setEditingProvider(null);
      fetchProviders();
    } catch (error) {
      message.error('保存服务商失败');
    }
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => (
        <Space>
          <span className="font-semibold">{text}</span>
          {text === defaultProvider && <Tag color="blue">默认</Tag>}
        </Space>
      )
    },
    {
      title: '模型',
      dataIndex: 'model',
      key: 'model',
    },
    {
      title: 'API 地址',
      dataIndex: 'api_url',
      key: 'api_url',
      ellipsis: true,
    },
    {
      title: '状态',
      dataIndex: 'enabled',
      key: 'enabled',
      render: (enabled: boolean) => (
        <Badge status={enabled ? 'success' : 'error'} text={enabled ? '已启用' : '已禁用'} />
      )
    },
    {
      title: '操作',
      key: 'actions',
      render: (_: any, record: Provider) => (
        <Space size="middle">
          <Tooltip title="设为默认">
            <Button 
              type="text" 
              icon={record.name === defaultProvider ? <StarFilled className="text-yellow-500" /> : <StarOutlined />} 
              onClick={() => handleSetDefault(record.name)}
              disabled={record.name === defaultProvider}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button 
              type="text" 
              icon={<EditOutlined className="text-blue-500" />} 
              onClick={() => handleEdit(record)}
            />
          </Tooltip>
          <Tooltip title="删除">
            <Button 
              type="text" 
              danger 
              icon={<DeleteOutlined />} 
              onClick={() => handleDelete(record.name)}
            />
          </Tooltip>
        </Space>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold m-0">AI 服务商管理</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          添加服务商
        </Button>
      </div>

      <Table 
        columns={columns} 
        dataSource={providers} 
        rowKey="name" 
        loading={loading}
        pagination={false}
        className="shadow-sm rounded-lg overflow-hidden border border-gray-100"
      />

      <Modal
        title={editingProvider ? "编辑服务商" : "添加服务商"}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          initialValues={{ enabled: true, max_tokens: 512, temperature: 0.1 }}
        >
          <Form.Item name="name" label="名称 (ID)" rules={[{ required: true }]}>
            <Input placeholder="例如：openai" disabled={!!editingProvider} />
          </Form.Item>
          
          <Form.Item name="api_key" label="API 密钥" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
          
          <Form.Item name="api_url" label="API 地址" rules={[{ required: true }]}>
            <Input placeholder="https://api.openai.com/v1" />
          </Form.Item>
          
          <Form.Item name="model" label="模型" rules={[{ required: true }]}>
            <Input placeholder="gpt-3.5-turbo" />
          </Form.Item>

          <div className="grid grid-cols-2 gap-4">
             <Form.Item name="max_tokens" label="最大 Token 数">
                <InputNumber className="w-full" />
             </Form.Item>
             <Form.Item name="temperature" label="随机性 (Temperature)">
                <InputNumber className="w-full" step={0.1} min={0} max={2} />
             </Form.Item>
          </div>

          <Form.Item name="enabled" label="已启用" valuePropName="checked">
            <Switch />
          </Form.Item>

          <div className="flex justify-end gap-2 mt-4">
            <Button onClick={() => setIsModalOpen(false)}>取消</Button>
            <Button type="primary" htmlType="submit">保存</Button>
          </div>
        </Form>
      </Modal>
    </div>
  );
};

export default Providers;