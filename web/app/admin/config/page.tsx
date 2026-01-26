"use client";

import React from "react";
import {
  PageContainer,
  ProForm,
  ProFormText,
  ProFormSwitch,
  ProFormDigit,
  ProCard,
} from "@ant-design/pro-components";
import { App } from "antd";

export default function ConfigPage() {
  const { message } = App.useApp();

  return (
    <PageContainer>
      <ProForm
        onFinish={async (values) => {
          try {
            const res = await fetch("/api/v1/admin/config/", {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(values),
            });
            if (res.ok) {
              message.success("配置更新成功");
            } else {
              message.error("更新失败");
            }
          } catch (e) {
            message.error("请求失败");
          }
        }}
        params={{}}
        request={async () => {
          const res = await fetch("/api/v1/admin/config/");
          return await res.json();
        }}
      >
        <ProCard
          title="应用配置"
          headerBordered
          collapsible
          style={{ marginBottom: 16 }}
        >
          <ProForm.Group>
            <ProFormText name={["app", "name"]} label="应用名称" />
            <ProFormText name={["app", "version"]} label="版本号" disabled />
            <ProFormSwitch name={["app", "debug"]} label="调试模式" />
          </ProForm.Group>
        </ProCard>

        <ProCard
          title="服务器配置"
          headerBordered
          collapsible
          style={{ marginBottom: 16 }}
        >
          <ProForm.Group>
            <ProFormText name={["server", "host"]} label="监听地址" />
            <ProFormDigit name={["server", "port"]} label="端口" />
          </ProForm.Group>
        </ProCard>

        <ProCard
          title="AI 配置"
          headerBordered
          collapsible
          style={{ marginBottom: 16 }}
        >
          <ProForm.Group>
            <ProFormText name={["ai", "default_provider"]} label="默认提供商" />
            <ProFormDigit name={["ai", "timeout"]} label="超时时间(s)" />
            <ProFormDigit name={["ai", "max_retries"]} label="重试次数" />
          </ProForm.Group>
        </ProCard>

        <ProCard
          title="限流配置"
          headerBordered
          collapsible
          style={{ marginBottom: 16 }}
        >
          <ProForm.Group>
            <ProFormSwitch name={["rate_limit", "enabled"]} label="启用限流" />
            <ProFormDigit
              name={["rate_limit", "per_minute"]}
              label="每分钟限额"
            />
          </ProForm.Group>
        </ProCard>
      </ProForm>
    </PageContainer>
  );
}
