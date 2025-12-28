import React, { useEffect, useState } from 'react';
import { Table, Button, Card, Modal, Form, Input, message, Tag, Typography, Tooltip, Space } from 'antd';
import { PlusOutlined, DeleteOutlined, CopyOutlined } from '@ant-design/icons';
import api from '../utils/api';
import dayjs from 'dayjs';

const { Title } = Typography;

interface ApiKey {
  id: number;
  key: string;
  name: string;
  enabled: boolean;
  usage_count: number;
  last_used_at: string | null;
  created_at: string;
}

const Keys: React.FC = () => {
  const [keys, setKeys] = useState<ApiKey[]>([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();

  const fetchKeys = async () => {
    setLoading(true);
    try {
      const { data } = await api.get('/keys');
      setKeys(data);
    } catch (error) {
      message.error('加载密钥失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKeys();
  }, []);

  const handleCreate = async (values: any) => {
    try {
      const key = values.key || Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      await api.post('/keys', { key, name: values.name });
      message.success('密钥创建成功');
      setIsModalOpen(false);
      form.resetFields();
      fetchKeys();
    } catch (error) {
      message.error('创建密钥失败');
    }
  };

  const handleDelete = async (key: string) => {
    Modal.confirm({
      title: '确认删除？',
      content: '删除后无法恢复，该密钥将失效。',
      okType: 'danger',
      onOk: async () => {
        try {
          await api.delete(`/keys/${key}`);
          message.success('密钥已删除');
          fetchKeys();
        } catch (error) {
          message.error('删除失败');
        }
      }
    });
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <span className="font-medium">{text}</span>
    },
    {
      title: '密钥 (Key)',
      dataIndex: 'key',
      key: 'key',
      render: (text: string) => (
        <Space>
          <code className="bg-gray-100 px-2 py-1 rounded text-blue-600 font-mono">{text}</code>
          <Tooltip title="复制">
             <Button 
               type="text" 
               icon={<CopyOutlined />} 
               size="small"
               onClick={() => {
                 navigator.clipboard.writeText(text);
                 message.success('已复制');
               }} 
             />
          </Tooltip>
        </Space>
      )
    },
    {
      title: '状态',
      dataIndex: 'enabled',
      key: 'enabled',
      render: (enabled: boolean) => (
        <Tag color={enabled ? 'success' : 'error'}>{enabled ? '已启用' : '已禁用'}</Tag>
      )
    },
    {
      title: '使用次数',
      dataIndex: 'usage_count',
      key: 'usage_count',
      render: (count: number) => <Tag color="blue">{count}</Tag>
    },
    {
      title: '最后使用',
      dataIndex: 'last_used_at',
      key: 'last_used_at',
      render: (text: string) => text ? <span className="text-gray-500">{dayjs(text).fromNow()}</span> : <span className="text-gray-300">-</span>
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text: string) => <span className="text-gray-500">{dayjs(text).format('YYYY-MM-DD HH:mm')}</span>
    },
    {
      title: '操作',
      key: 'actions',
      render: (_: any, record: ApiKey) => (
        <Button 
          type="text" 
          danger 
          icon={<DeleteOutlined />} 
          onClick={() => handleDelete(record.key)} 
        />
      )
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <Title level={2} style={{ margin: 0 }}>密钥管理</Title>
          <span className="text-gray-500">管理 API 访问凭证</span>
        </div>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>
          创建密钥
        </Button>
      </div>

      <Card className="shadow-sm rounded-xl border-gray-100" styles={{ body: { padding: 0 } }}>
        <Table
          columns={columns}
          dataSource={keys}
          rowKey="id"
          loading={loading}
          pagination={false}
          className="overflow-hidden rounded-xl"
        />
      </Card>

      <Modal
        title="创建新密钥"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreate}
        >
          <Form.Item name="name" label="名称/备注" rules={[{ required: true }]}>
            <Input placeholder="例如：我的设备1" />
          </Form.Item>
          
          <Form.Item name="key" label="自定义 Key (可选)">
             <Input placeholder="留空则自动生成" />
          </Form.Item>

          <div className="flex justify-end gap-2 mt-4">
            <Button onClick={() => setIsModalOpen(false)}>取消</Button>
            <Button type="primary" htmlType="submit">创建</Button>
          </div>
        </Form>
      </Modal>
    </div>
  );
};

export default Keys;