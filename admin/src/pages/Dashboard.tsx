import React, { useEffect, useState } from 'react';
import { Card, Statistic, Row, Col, message, Typography, Tooltip } from 'antd';
import { CloudServerOutlined, ReloadOutlined, InfoCircleOutlined, RiseOutlined } from '@ant-design/icons';
import api from '../utils/api';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/zh-cn';

dayjs.extend(relativeTime);
dayjs.locale('zh-cn');

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts';

interface Stat {
  provider_name: string;
  call_count: number;
  last_called_at: string;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<Stat[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const { data } = await api.get('/stats');
      setStats(data);
    } catch (error) {
      message.error('加载统计失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const totalCalls = stats.reduce((acc, curr) => acc + curr.call_count, 0);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold m-0">仪表盘概览</h2>
          <span className="text-gray-500">实时系统统计</span>
        </div>
        <Card className="cursor-pointer hover:shadow-md transition-all rounded-full px-4 py-1" size="small" onClick={fetchStats} variant="borderless">
          <ReloadOutlined spin={loading} className="text-blue-500" /> <span className="ml-2 font-medium">刷新数据</span>
        </Card>
      </div>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
           <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
              <Card className="shadow-sm border-none bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl">
                <Statistic
                  title={<span className="text-blue-100">API 调用总数</span>}
                  value={totalCalls}
                  prefix={<CloudServerOutlined />}
                  // @ts-ignore
                  styles={{ content: { color: 'black', fontWeight: 'bold' } }}
                />
              </Card>
              <Card className="shadow-sm border-none bg-white rounded-xl">
                 <Statistic
                  title={<span className="text-gray-500">活跃服务商</span>}
                  value={stats.length}
                  prefix={<RiseOutlined className="text-green-500" />}
                  // @ts-ignore
                  styles={{ content: { fontWeight: 'bold' } }}
                />
              </Card>
           </div>
           
           <Card title="服务商调用分布" className="shadow-sm border-gray-100 rounded-xl" variant="borderless">
             <div className="h-[300px] w-full min-h-[300px]">
               <ResponsiveContainer width="100%" height="100%">
                 <BarChart data={stats}>
                   <CartesianGrid strokeDasharray="3 3" vertical={false} />
                   <XAxis dataKey="provider_name" axisLine={false} tickLine={false} />
                   <YAxis axisLine={false} tickLine={false} />
                   <RechartsTooltip 
                      cursor={{fill: '#f3f4f6'}}
                      contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                   />
                   <Bar dataKey="call_count" fill="#1677ff" radius={[4, 4, 0, 0]}>
                      {stats.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                   </Bar>
                 </BarChart>
               </ResponsiveContainer>
             </div>
           </Card>
        </Col>
        
        <Col xs={24} lg={8}>
          <Card title="最近活动" className="shadow-sm border-gray-100 rounded-xl h-full" variant="borderless">
             <div className="space-y-4">
                {stats.sort((a,b) => new Date(b.last_called_at).getTime() - new Date(a.last_called_at).getTime()).map((stat, idx) => (
                  <div key={stat.provider_name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-blue-50 transition-colors">
                    <div className="flex items-center gap-3">
                       <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS[idx % COLORS.length] }}></div>
                       <div>
                         <div className="font-semibold text-gray-700">{stat.provider_name}</div>
                         <div className="text-xs text-gray-400">{dayjs(stat.last_called_at).fromNow()}</div>
                       </div>
                    </div>
                    <div className="font-mono font-medium text-blue-600">
                      {stat.call_count}
                    </div>
                  </div>
                ))}
                {stats.length === 0 && (
                   <div className="text-center text-gray-400 py-8">暂无活动记录</div>
                )}
             </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;