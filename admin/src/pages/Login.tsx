import React, { useState } from 'react';
import { Form, Input, Button, Card, Typography, App } from 'antd';
import { UserOutlined, LockOutlined, ThunderboltFilled } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';

const { Title, Text } = Typography;

const Login: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();
  const { message } = App.useApp();

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      const { data } = await api.post('/login', values);
      login(data.access_token);
      message.success('欢迎回来！');
      navigate('/dashboard');
    } catch (error) {
      message.error('凭证无效，请重试。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f172a] relative overflow-hidden">
      {/* Animated Background Elements */}
      <motion.div 
        animate={{ 
          scale: [1, 1.2, 1],
          rotate: [0, 90, 0],
          opacity: [0.3, 0.5, 0.3]
        }}
        transition={{ duration: 20, repeat: Infinity }}
        className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-blue-600/20 blur-[100px]"
      />
      <motion.div 
        animate={{ 
          scale: [1, 1.3, 1],
          rotate: [0, -60, 0],
          opacity: [0.2, 0.4, 0.2]
        }}
        transition={{ duration: 25, repeat: Infinity, delay: 2 }}
        className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] rounded-full bg-purple-600/20 blur-[120px]"
      />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="z-10 w-full max-w-md px-4"
      >
        <Card className="shadow-2xl border-none backdrop-blur-xl bg-white/5 overflow-hidden ring-1 ring-white/10">
          <div className="text-center mb-10 mt-4">
            <motion.div 
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 260, damping: 20 }}
              className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 text-white mb-6 shadow-lg shadow-blue-500/30"
            >
              <ThunderboltFilled style={{ fontSize: '32px' }} />
            </motion.div>
            <Title level={2} style={{ margin: 0, color: 'white', fontWeight: 700 }}>OCS 管理系统</Title>
            <Text className="text-gray-400 block mt-2">登录以管理您的 AI 基础设施</Text>
          </div>

          <Form
            name="login"
            onFinish={onFinish}
            layout="vertical"
            size="large"
            className="login-form"
          >
            <Form.Item
              name="username"
              rules={[{ required: true, message: '请输入用户名' }]}
            >
              <Input 
                prefix={<UserOutlined className="text-gray-400" />} 
                placeholder="用户名" 
                className="bg-white/5 border-white/10 text-white hover:border-blue-500 focus:border-blue-500 hover:bg-white/10 placeholder-gray-500"
                style={{ color: 'white' }}
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[{ required: true, message: '请输入密码' }]}
            >
              <Input.Password 
                prefix={<LockOutlined className="text-gray-400" />} 
                placeholder="密码"
                className="bg-white/5 border-white/10 text-white hover:border-blue-500 focus:border-blue-500 hover:bg-white/10 placeholder-gray-500"
                style={{ color: 'white' }} 
              />
            </Form.Item>

            <Form.Item>
              <Button 
                type="primary" 
                htmlType="submit" 
                block 
                loading={loading} 
                className="h-12 text-base font-semibold bg-gradient-to-r from-blue-600 to-purple-600 border-none hover:shadow-lg hover:shadow-blue-500/25 transition-all duration-300"
              >
                登录
              </Button>
            </Form.Item>
          </Form>
        </Card>
        
        <div className="text-center mt-6 text-gray-500 text-sm">
           &copy; {new Date().getFullYear()} OCS 题库系统
        </div>
      </motion.div>
    </div>
  );
};

export default Login;