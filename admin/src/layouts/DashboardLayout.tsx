import React, { useState } from 'react';
import { Layout, Menu, Button, theme, Avatar, Dropdown, Breadcrumb } from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DashboardOutlined,
  CloudServerOutlined,
  LogoutOutlined,
  UserOutlined,
  SettingOutlined,
  FileTextOutlined,
  LineChartOutlined,
  KeyOutlined
} from '@ant-design/icons';
import { Outlet, useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const { Header, Sider, Content } = Layout;

const DashboardLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const { token: { colorBgContainer, borderRadiusLG } } = theme.useToken();
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();

  const handleMenuClick = (key: string) => {
    navigate(key);
  };

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: '仪表盘',
    },
    {
      key: '/dashboard/providers',
      icon: <CloudServerOutlined />,
      label: 'AI 服务商',
    },
    {
      key: '/dashboard/keys',
      icon: <KeyOutlined />,
      label: '密钥管理',
    },
    {
      key: '/dashboard/logs',
      icon: <FileTextOutlined />,
      label: '调用日志',
    },
    {
      key: '/dashboard/analysis',
      icon: <LineChartOutlined />,
      label: '数据分析',
    },
    {
      key: '/dashboard/settings',
      icon: <SettingOutlined />,
      label: '系统设置',
    },
  ];

  const userMenu = {
    items: [
      {
        key: 'settings',
        label: '设置',
        icon: <SettingOutlined />,
        onClick: () => navigate('/dashboard/settings')
      },
      {
        type: 'divider'
      },
      {
        key: 'logout',
        label: '退出登录',
        icon: <LogoutOutlined />,
        danger: true,
        onClick: () => {
          logout();
          navigate('/login');
        }
      }
    ]
  };

  // Generate breadcrumb items
  const pathSnippets = location.pathname.split('/').filter((i) => i && i !== 'dashboard');
  const breadcrumbItems = [
    { title: <Link to="/dashboard">仪表盘</Link> },
    ...pathSnippets.map((_, index) => {
      return {
        title: <span className="capitalize">{pathSnippets[index]}</span>,
      };
    }),
  ];

  return (
    <Layout className="min-h-screen">
      <Sider 
        trigger={null} 
        collapsible 
        collapsed={collapsed} 
        className="shadow-xl z-20 border-r border-gray-100 dark:border-gray-800"
        width={240}
        theme="light"
      >
        <div className="flex items-center justify-center h-16 m-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-blue-200 shadow-md overflow-hidden">
           {collapsed ? (
             <div className="text-white font-bold text-lg">OCS</div>
           ) : (
             <h1 className="text-white font-bold text-lg tracking-wide m-0">OCS 管理后台</h1>
           )}
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => handleMenuClick(key)}
          className="border-none px-2"
        />
      </Sider>
      <Layout>
        <Header style={{ padding: 0, background: colorBgContainer }} className="flex justify-between items-center px-6 sticky top-0 z-10 shadow-sm/50 border-b border-gray-100">
          <div className="flex items-center gap-4">
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              className="hover:bg-gray-100 rounded-lg w-10 h-10 flex items-center justify-center"
            />
            <Breadcrumb items={breadcrumbItems} className="hidden md:flex" />
          </div>
          <div className="flex items-center gap-4">
             <Dropdown menu={userMenu as any} placement="bottomRight" arrow>
                <div className="flex items-center gap-3 cursor-pointer hover:bg-gray-50 p-1.5 px-3 rounded-full transition-all border border-transparent hover:border-gray-100">
                  <Avatar 
                    icon={<UserOutlined />} 
                    style={{ backgroundColor: '#1677ff' }} 
                    className="shadow-sm"
                  />
                  <div className="hidden sm:block text-left">
                    <div className="text-sm font-semibold text-gray-700 leading-tight">管理员</div>
                    <div className="text-xs text-gray-400">系统管理员</div>
                  </div>
                </div>
             </Dropdown>
          </div>
        </Header>
        <Content
          className="overflow-y-auto bg-gray-50/50"
          style={{
            margin: 0,
            padding: 24,
            minHeight: 280,
            borderRadius: borderRadiusLG
          }}
        >
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default DashboardLayout;
