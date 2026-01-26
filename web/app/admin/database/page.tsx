"use client";

import React, { useState, useEffect } from "react";
import {
  PageContainer,
  ProCard,
  StatisticCard,
} from "@ant-design/pro-components";
import { Button, App, Space } from "antd";
import { DatabaseOutlined, SaveOutlined } from "@ant-design/icons";

const { Statistic } = StatisticCard;

export default function DatabasePage() {
  const [stats, setStats] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const { message } = App.useApp();

  const fetchStats = async () => {
    try {
      const res = await fetch("/api/v1/admin/database/stats");
      const data = await res.json();
      setStats(data);
    } catch (e) {
      message.error("获取统计信息失败");
    }
  };

  const handleBackup = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/v1/admin/database/backup", {
        method: "POST",
      });
      const data = await res.json();
      if (res.ok) {
        message.success(`备份成功: ${data.path}`);
      } else {
        message.error(data.detail || "备份失败");
      }
    } catch (e) {
      message.error("请求失败");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <PageContainer>
      <ProCard
        title="数据库概览"
        extra={
          <Button
            type="primary"
            icon={<SaveOutlined />}
            onClick={handleBackup}
            loading={loading}
          >
            立即备份
          </Button>
        }
      >
        <ProCard.Group title="核心指标" direction="row">
          <ProCard>
            <Statistic
              title="数据库类型"
              value={stats.type || "Unknown"}
              icon={<DatabaseOutlined />}
            />
          </ProCard>
          <ProCard>
            <Statistic
              title="文件大小"
              value={stats.size_mb ? `${stats.size_mb} MB` : "-"}
              description="仅 SQLite"
            />
          </ProCard>
          <ProCard>
            <Statistic title="总题目数" value={stats.questions || 0} />
          </ProCard>
          <ProCard>
            <Statistic title="总用户数" value={stats.users || 0} />
          </ProCard>
        </ProCard.Group>
      </ProCard>
    </PageContainer>
  );
}
