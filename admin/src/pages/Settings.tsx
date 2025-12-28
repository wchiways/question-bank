import React, { useEffect, useState } from 'react';
import { Form, Input, InputNumber, Button, Card, Switch, message, Divider, Tabs, Typography, Alert } from 'antd';
import { SaveOutlined, SafetyCertificateOutlined, SettingOutlined, CloudOutlined } from '@ant-design/icons';
import api from '../utils/api';

const { Title } = Typography;

const Settings: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const { data } = await api.get('/config');
      form.setFieldsValue(data);
    } catch (error) {
      message.error('加载配置失败');
    } finally {
      setInitialLoading(false);
    }
  };

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      await api.post('/config', values);
      message.success('配置已更新');
    } catch (error) {
      message.error('更新配置失败');
    } finally {
      setLoading(false);
    }
  };

  const items = [
    {
      key: '1',
      label: (<span><SettingOutlined /> 常规设置</span>),
      children: (
        <div className="max-w-2xl">
          {/* @ts-ignore */}
          <Divider orientation="left">应用设置</Divider>
          <Form.Item name={['app', 'name']} label="系统名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name={['app', 'debug']} label="调试模式" valuePropName="checked">
            <Switch />
          </Form.Item>
          <Form.Item name={['app', 'api_v1_prefix']} label="API 前缀">
            <Input disabled />
          </Form.Item>
        </div>
      ),
    },
    {
      key: '2',
      label: (<span><CloudOutlined /> 速率限制</span>),
      children: (
        <div className="max-w-2xl">
           <Alert message="速率限制有助于保护您的 API 免受滥用。" type="info" showIcon className="mb-6" />
           <Form.Item name={['rate_limit', 'enabled']} label="启用速率限制" valuePropName="checked">
            <Switch />
          </Form.Item>
          <Form.Item name={['rate_limit', 'per_minute']} label="每分钟请求数">
            <InputNumber min={1} />
          </Form.Item>
        </div>
      ),
    },
    {
      key: '3',
      label: (<span><SafetyCertificateOutlined /> 安全设置</span>),
      children: (
        <div className="max-w-2xl">
           <Alert message="修改凭证将需要您重新登录。" type="warning" showIcon className="mb-6" />
           <Form.Item name={['security', 'admin_username']} label="管理员用户名" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name={['security', 'admin_password']} label="管理员密码" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
          <Form.Item name={['security', 'secret_key']} label="密钥 (Secret Key)" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <Title level={2} style={{ margin: 0 }}>系统设置</Title>
          <span className="text-gray-500">管理全局配置</span>
        </div>
        <Button 
          type="primary" 
          icon={<SaveOutlined />} 
          loading={loading}
          onClick={() => form.submit()}
          size="large"
        >
          保存更改
        </Button>
      </div>

      <Card className="shadow-sm rounded-xl border-gray-100" loading={initialLoading}>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{}}
        >
          <Tabs defaultActiveKey="1" items={items} size="large" />
        </Form>
      </Card>
    </div>
  );
};

export default Settings;