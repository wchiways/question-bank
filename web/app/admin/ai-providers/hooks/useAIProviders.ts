"use client";

import { useState, useEffect, useCallback } from "react";
import { AIProvider, AIConfig, TestResult, UsageInfo } from "../../types";

interface TestResultWithUsage extends TestResult {
  usage?: UsageInfo;
}

export function useAIProviders() {
  const [config, setConfig] = useState<AIConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [testing, setTesting] = useState<Record<string, boolean>>({});

  const loadConfig = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/v1/admin/ai/providers");
      const data = await res.json();
      setConfig(data);
    } catch (e) {
      console.error("加载配置失败:", e);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateProvider = useCallback(
    async (providerKey: string, values: Partial<AIProvider>) => {
      try {
        const res = await fetch(`/api/v1/admin/ai/providers/${providerKey}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(values),
        });

        if (res.ok) {
          await loadConfig();
          return true;
        }
        return false;
      } catch (e) {
        console.error("更新配置失败:", e);
        return false;
      }
    },
    [loadConfig],
  );

  const testProvider = useCallback(
    async (providerKey: string): Promise<TestResult> => {
      setTesting((prev) => ({ ...prev, [providerKey]: true }));

      try {
        const res = await fetch(
          `/api/v1/admin/ai/providers/${providerKey}/test`,
          {
            method: "POST",
          },
        );
        const result = await res.json();
        return result;
      } catch (e) {
        return {
          success: false,
          provider: providerKey,
          error: "测试请求失败",
        };
      } finally {
        setTesting((prev) => ({ ...prev, [providerKey]: false }));
      }
    },
    [],
  );

  const setDefaultProvider = useCallback(
    async (providerKey: string) => {
      try {
        const res = await fetch("/api/v1/admin/ai/default-provider", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(providerKey),
        });

        if (res.ok) {
          await loadConfig();
          return true;
        }
        return false;
      } catch (e) {
        console.error("设置默认提供商失败:", e);
        return false;
      }
    },
    [loadConfig],
  );

  const batchEnable = useCallback(
    async (providerKeys: string[]) => {
      try {
        const res = await fetch("/api/v1/admin/ai/providers/batch-enable", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ provider_keys: providerKeys }),
        });

        if (res.ok) {
          await loadConfig();
          return true;
        }
        return false;
      } catch (e) {
        console.error("批量启用失败:", e);
        return false;
      }
    },
    [loadConfig],
  );

  const batchDisable = useCallback(
    async (providerKeys: string[]) => {
      try {
        const res = await fetch("/api/v1/admin/ai/providers/batch-disable", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ provider_keys: providerKeys }),
        });

        if (res.ok) {
          await loadConfig();
          return true;
        }
        return false;
      } catch (e) {
        console.error("批量禁用失败:", e);
        return false;
      }
    },
    [loadConfig],
  );

  const createProvider = useCallback(
    async (providerData: Omit<AIProvider, "key"> & { key: string }) => {
      try {
        const res = await fetch("/api/v1/admin/ai/providers", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(providerData),
        });

        if (res.ok) {
          await loadConfig();
          return true;
        }
        const error = await res.json();
        console.error("创建服务商失败:", error);
        return false;
      } catch (e) {
        console.error("创建服务商失败:", e);
        return false;
      }
    },
    [loadConfig],
  );

  const deleteProvider = useCallback(
    async (providerKey: string) => {
      try {
        const res = await fetch(`/api/v1/admin/ai/providers/${providerKey}`, {
          method: "DELETE",
        });

        if (res.ok) {
          await loadConfig();
          return true;
        }
        const error = await res.json();
        console.error("删除服务商失败:", error);
        return false;
      } catch (e) {
        console.error("删除服务商失败:", e);
        return false;
      }
    },
    [loadConfig],
  );

  useEffect(() => {
    loadConfig();
  }, [loadConfig]);

  return {
    config,
    loading,
    testing,
    reload: loadConfig,
    updateProvider,
    testProvider,
    setDefaultProvider,
    batchEnable,
    batchDisable,
    createProvider,
    deleteProvider,
  };
}
