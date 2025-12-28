import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Typography, Select, App } from 'antd';
import api from '../utils/api';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, Legend } from 'recharts';

const { Title } = Typography;
const { Option } = Select;

interface TrendData {
  date: string;
  count: number;
  avg_latency: number;
}

const Analysis: React.FC = () => {
  const [trendData, setTrendData] = useState<TrendData[]>([]);
  const [days, setDays] = useState(7);
  const [loading, setLoading] = useState(false);
  const { message } = App.useApp();

  const fetchTrend = async () => {
    setLoading(true);
    try {
      const { data } = await api.get(`/analysis/trend?days=${days}`);
      setTrendData(data);
    } catch (error) {
      message.error('加载分析数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrend();
  }, [days]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <Title level={2} style={{ margin: 0 }}>数据分析</Title>
          <span className="text-gray-500">API 调用趋势与性能分析</span>
        </div>
        <Select value={days} onChange={setDays} style={{ width: 120 }}>
          <Option value={7}>最近 7 天</Option>
          <Option value={14}>最近 14 天</Option>
          <Option value={30}>最近 30 天</Option>
        </Select>
      </div>

      <Row gutter={[24, 24]}>
        <Col span={24}>
          <Card title="调用量趋势" className="shadow-sm border-gray-100 rounded-xl" bordered={false}>
            <div className="h-[350px] w-full min-h-[350px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trendData}>
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#1677ff" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#1677ff" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="date" />
                  <YAxis />
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <RechartsTooltip 
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Area type="monotone" dataKey="count" stroke="#1677ff" fillOpacity={1} fill="url(#colorCount)" name="调用次数" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>

        <Col span={24}>
          <Card title="平均延迟 (ms)" className="shadow-sm border-gray-100 rounded-xl" bordered={false}>
            <div className="h-[350px] w-full min-h-[350px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trendData}>
                  <XAxis dataKey="date" />
                  <YAxis />
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <RechartsTooltip 
                    cursor={{fill: '#f3f4f6'}}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Bar dataKey="avg_latency" fill="#82ca9d" name="平均延迟" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Analysis;
