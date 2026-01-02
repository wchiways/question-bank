'use client';

import React from 'react';
import dynamic from 'next/dynamic';
import {
  BookOutlined,
  BarChartOutlined,
  SettingOutlined,
  DatabaseOutlined,
  DashboardOutlined,
  ThunderboltOutlined
} from '@ant-design/icons';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { AntdRegistry } from '@ant-design/nextjs-registry';
import { ConfigProvider, Spin, App } from 'antd';
import zhCN from 'antd/locale/zh_CN';

const ProLayout = dynamic(
  () => import('@ant-design/pro-components').then((mod) => mod.ProLayout),
  {
    ssr: false,
    loading: () => (
      <div style={{ height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Spin size="large" />
      </div>
    ),
  },
);

const menuData = [
  {
    path: '/admin',
    name: '控制台',
    icon: <DashboardOutlined />,
  },
  {
    path: '/admin/questions',
    name: '题库管理',
    icon: <BookOutlined />,
  },
  {
    path: '/admin/ai-providers',
    name: 'AI 服务商',
    icon: <ThunderboltOutlined />,
  },
  {
    path: '/admin/stats',
    name: '统计分析',
    icon: <BarChartOutlined />,
  },
  {
    path: '/admin/config',
    name: '系统配置',
    icon: <SettingOutlined />,
  },
  {
    path: '/admin/database',
    name: '数据库管理',
    icon: <DatabaseOutlined />,
  },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <AntdRegistry>
      <ConfigProvider locale={zhCN}>
        <App>
          <div
            style={{
              height: '100vh',
            }}
          >
            <ProLayout
              title="OCS-TIKU 管理后台"
              logo="/favicon.svg"
              location={{
                pathname,
              }}
              menuDataRender={() => menuData}
              menuItemRender={(item, dom) => (
                <Link href={item.path || '/admin'}>{dom}</Link>
              )}
              layout="mix"
              fixedHeader
              fixSiderbar
            >
              {children}
            </ProLayout>
          </div>
        </App>
      </ConfigProvider>
    </AntdRegistry>
  );
}
