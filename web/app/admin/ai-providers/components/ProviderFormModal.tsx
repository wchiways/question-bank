'use client';

import React, { useEffect } from 'react';
import { Modal, Form, Input, Slider, Tabs } from 'antd';

interface Props {
  visible: boolean;
  provider: any;
  onSubmit: (values: any) => Promise<boolean>;
  onCancel: () => void;
}

export const ProviderFormModal: React.FC<Props> = ({
  visible,
  provider,
  onSubmit,
  onCancel,
}) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (visible && provider) {
      form.setFieldsValue(provider);
    }
  }, [visible, provider, form]);

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      const success = await onSubmit(values);
      if (success) {
        form.resetFields();
      }
      return success;
    } catch (e) {
      return false;
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onCancel();
  };

  if (!visible || !provider) {
    return null;
  }

  return (
    <Modal
      title={`配置 ${provider.name}`}
      open={visible}
      onOk={handleOk}
      onCancel={handleCancel}
      width={700}
      destroyOnHidden
      okText="保存"
      cancelText="取消"
    >
      <Form
        form={form}
        layout="vertical"
      >
        <Tabs
          items={[
            {
              key: 'basic',
              label: '基础配置',
              children: (
                <>
                  <Form.Item
                    label="服务商名称"
                    name="name"
                  >
                    <Input disabled />
                  </Form.Item>

                  <Form.Item
                    label="API Key"
                    name="api_key"
                    rules={[{ required: true, message: '请输入 API Key' }]}
                    extra="您的密钥将被安全加密存储"
                  >
                    <Input.Password
                      placeholder="sk-..."
                      visibilityToggle
                    />
                  </Form.Item>

                  <Form.Item
                    label="API 地址"
                    name="api_url"
                    rules={[{ required: true, message: '请输入 API 地址' }]}
                  >
                    <Input placeholder="https://api.example.com/v1/chat/completions" />
                  </Form.Item>
                </>
              ),
            },
            {
              key: 'advanced',
              label: '高级参数',
              children: (
                <>
                  <Form.Item
                    label="模型名称"
                    name="model"
                    rules={[{ required: true, message: '请输入模型名称' }]}
                    extra="请确保服务商支持该模型"
                  >
                    <Input placeholder="gpt-3.5-turbo" />
                  </Form.Item>

                  <Form.Item
                    label="最大 Tokens"
                    name="max_tokens"
                    extra="控制返回的最大 token 数量"
                  >
                    <Slider
                      min={100}
                      max={8000}
                      step={100}
                      marks={{
                        100: '100',
                        1000: '1K',
                        4000: '4K',
                        8000: '8K',
                      }}
                    />
                  </Form.Item>

                  <Form.Item
                    label="温度 (Temperature)"
                    name="temperature"
                    extra="控制输出的随机性，值越高输出越随机"
                  >
                    <Slider
                      min={0}
                      max={2}
                      step={0.1}
                      marks={{
                        0: '精确',
                        0.7: '平衡',
                        1.5: '创意',
                        2: '随机',
                      }}
                    />
                  </Form.Item>
                </>
              ),
            },
          ]}
        />
      </Form>
    </Modal>
  );
};
