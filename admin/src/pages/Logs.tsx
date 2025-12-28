import React, { useEffect, useState } from 'react';
import { Table, Tag, Card, Typography, Tooltip, App } from 'antd';
import { ClockCircleOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import api from '../utils/api';
import dayjs from 'dayjs';

const { Title } = Typography;

interface Log {
  id: number;
  provider: string;
  model: string;
  prompt_length: number;
  response_length: number;
  latency_ms: number;
  success: boolean;
  created_at: string;
  error_message?: string;
}

const Logs: React.FC = () => {
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });
  const { message } = App.useApp();

  const fetchLogs = async (page: int = 1) => {
    setLoading(true);
    try {
      // Offset based pagination
      const skip = (page - 1) * 20;
      const { data } = await api.get(`/logs?skip=${skip}&limit=20`);
      setLogs(data);
      // Assuming infinite scroll or simple next/prev if total not provided
    } catch (error) {
      message.error('加载日志失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const columns = [
    {
      title: '时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (text: string) => <span className="text-gray-500">{dayjs(text).format('YYYY-MM-DD HH:mm:ss')}</span>,
    },
    {
      title: '服务商',
      dataIndex: 'provider',
      key: 'provider',
      render: (text: string) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: '模型',
      dataIndex: 'model',
      key: 'model',
      responsive: ['md'],
    },
    {
      title: '耗时',
      dataIndex: 'latency_ms',
      key: 'latency_ms',
      render: (ms: number) => (
        <span className={`${ms > 2000 ? 'text-orange-500' : 'text-green-600'} font-mono`}>
          {ms}ms
        </span>
      ),
    },
    {
      title: 'Token 消耗',
      key: 'tokens',
      render: (_: any, record: Log) => (
        <Tooltip title={`Prompt: ${record.prompt_length} / Response: ${record.response_length}`}>
          <span className="cursor-help text-gray-600">
             {record.prompt_length + record.response_length} chars
          </span>
        </Tooltip>
      ),
      responsive: ['lg'],
    },
    {
      title: '状态',
      dataIndex: 'success',
      key: 'success',
      render: (success: boolean, record: Log) => (
        success ? (
          <Tag icon={<CheckCircleOutlined />} color="success">成功</Tag>
        ) : (
          <Tooltip title={record.error_message}>
            <Tag icon={<CloseCircleOutlined />} color="error" className="cursor-help">失败</Tag>
          </Tooltip>
        )
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <Title level={2} style={{ margin: 0 }}>调用日志</Title>
          <span className="text-gray-500">查看详细的 API 调用记录</span>
        </div>
      </div>

      <Card className="shadow-sm rounded-xl border-gray-100" styles={{ body: { padding: 0 } }}>
        <Table
          columns={columns as any}
          dataSource={logs}
          rowKey="id"
          loading={loading}
          pagination={{
            current: pagination.current,
            pageSize: 20,
            onChange: (page) => {
              setPagination(prev => ({ ...prev, current: page }));
              fetchLogs(page);
            }
          }}
          className="overflow-hidden rounded-xl"
        />
      </Card>
    </div>
  );
};

export default Logs;
