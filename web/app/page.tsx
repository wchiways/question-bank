"use client";

import React from "react";
import { Button, Card, Col, Row, Space, Tag, Divider } from "antd";
import {
  RocketOutlined,
  DatabaseOutlined,
  RobotOutlined,
  BarChartOutlined,
  SafetyOutlined,
  ThunderboltOutlined,
  ArrowRightOutlined,
  CheckCircleOutlined,
  CodeOutlined,
  ApiOutlined,
  CloudServerOutlined,
  SettingOutlined,
} from "@ant-design/icons";
import Link from "next/link";

export default function HomePage() {
  const features = [
    {
      icon: <ThunderboltOutlined style={{ fontSize: 32, color: "#1890ff" }} />,
      title: "异步架构",
      description: "全链路异步处理，支持高并发，相比 Flask 版本性能提升 50 倍",
    },
    {
      icon: <SafetyOutlined style={{ fontSize: 32, color: "#52c41a" }} />,
      title: "类型安全",
      description: "100% 类型注解覆盖，Pydantic 数据验证，减少运行时错误",
    },
    {
      icon: <CodeOutlined style={{ fontSize: 32, color: "#faad14" }} />,
      title: "自动文档",
      description: "Swagger UI 和 ReDoc 自动生成，无需手动编写 API 文档",
    },
    {
      icon: <DatabaseOutlined style={{ fontSize: 32, color: "#722ed1" }} />,
      title: "分层设计",
      description: "清晰的 API、Service、Repository 三层架构，易于维护和扩展",
    },
    {
      icon: <RocketOutlined style={{ fontSize: 32, color: "#f5222d" }} />,
      title: "多 AI 平台",
      description: "支持硅基流动、阿里百炼、智谱 AI、Google、OpenAI 等多个平台",
    },
    {
      icon: <BarChartOutlined style={{ fontSize: 32, color: "#13c2c2" }} />,
      title: "三级缓存",
      description: "内存缓存 + 数据库 + AI 服务，智能重试机制，提升响应速度",
    },
  ];

  const techStack = [
    { name: "Python 3.11+", color: "blue" },
    { name: "FastAPI 0.127+", color: "teal" },
    { name: "SQLModel", color: "orange" },
    { name: "Next.js 13+", color: "geekblue" },
    { name: "SQLite", color: "green" },
    { name: "httpx", color: "purple" },
    { name: "loguru", color: "cyan" },
    { name: "uv", color: "red" },
  ];

  const quickLinks = [
    { title: "题库管理", href: "/admin/questions", icon: <DatabaseOutlined /> },
    { title: "AI 配置", href: "/admin/ai-providers", icon: <RobotOutlined /> },
    { title: "数据统计", href: "/admin/stats", icon: <BarChartOutlined /> },
    { title: "系统设置", href: "/admin/settings", icon: <SafetyOutlined /> },
  ];

  const fastapiFeatures = [
    {
      icon: <ThunderboltOutlined style={{ fontSize: 28, color: "#f5222d" }} />,
      title: "高性能异步",
      description:
        "基于 Starlette 和 Pydantic，提供原生异步支持，处理并发请求性能优异",
    },
    {
      icon: <CodeOutlined style={{ fontSize: 28, color: "#1890ff" }} />,
      title: "自动文档生成",
      description:
        "Swagger UI 和 ReDoc 自动生成，无需手动编写 API 文档，开箱即用",
    },
    {
      icon: <ApiOutlined style={{ fontSize: 28, color: "#52c41a" }} />,
      title: "类型验证",
      description: "使用 Pydantic 进行数据验证，自动类型检查，减少运行时错误",
    },
    {
      icon: <CloudServerOutlined style={{ fontSize: 28, color: "#722ed1" }} />,
      title: "依赖注入",
      description: "强大的依赖注入系统，优雅地管理数据库会话、认证等业务逻辑",
    },
    {
      icon: <SettingOutlined style={{ fontSize: 28, color: "#faad14" }} />,
      title: "模块化设计",
      description:
        "清晰的目录结构，Repository 模式分离数据访问层，易于维护和扩展",
    },
    {
      icon: <SafetyOutlined style={{ fontSize: 28, color: "#13c2c2" }} />,
      title: "安全可靠",
      description: "OAuth2 认证、CORS 中间件、SQL 注入防护，企业级安全保障",
    },
  ];

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%)",
        padding: "60px 20px",
      }}
    >
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        {/* Hero Section */}
        <div style={{ textAlign: "center", marginBottom: 80 }}>
          <h1
            style={{
              fontSize: 56,
              fontWeight: 700,
              color: "#1890ff",
              marginBottom: 24,
              marginTop: 0,
            }}
          >
            OCS 题库系统
          </h1>
          <p
            style={{
              fontSize: 24,
              color: "#595959",
              marginBottom: 32,
              maxWidth: 800,
              margin: "0 auto 40px",
            }}
          >
            智能在线考试管理平台
          </p>
          <p
            style={{
              fontSize: 16,
              color: "#8c8c8c",
              marginBottom: 40,
              maxWidth: 700,
              margin: "0 auto 40px",
            }}
          >
            基于 FastAPI + AsyncIO + SQLModel 的高性能题库查询系统，
            全链路异步处理支持高并发，相比 Flask 版本性能提升 50 倍。 支持多 AI
            平台智能答题，自动生成 API 文档，开箱即用。
          </p>
          <Space size="large">
            <Link href="/admin/questions">
              <Button
                type="primary"
                size="large"
                icon={<RocketOutlined />}
                style={{ height: 48, fontSize: 16, paddingHorizontal: 32 }}
              >
                开始使用
              </Button>
            </Link>
            <Link href="/admin/stats">
              <Button
                size="large"
                icon={<BarChartOutlined />}
                style={{ height: 48, fontSize: 16, paddingHorizontal: 32 }}
              >
                查看统计
              </Button>
            </Link>
          </Space>
        </div>

        {/* Features Section */}
        <div style={{ marginBottom: 80 }}>
          <h2
            style={{
              textAlign: "center",
              marginBottom: 48,
              color: "#262626",
              fontSize: 32,
              fontWeight: 600,
              marginTop: 0,
            }}
          >
            核心功能特性
          </h2>
          <Row gutter={[24, 24]}>
            {features.map((feature, index) => (
              <Col xs={24} sm={12} lg={8} key={index}>
                <Card
                  hoverable
                  style={{
                    height: "100%",
                    borderRadius: 12,
                    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                    transition: "all 0.3s",
                  }}
                  styles={{ body: { padding: 32 } }}
                >
                  <Space
                    direction="vertical"
                    size="middle"
                    style={{ width: "100%" }}
                  >
                    <div>{feature.icon}</div>
                    <div>
                      <h3
                        style={{
                          marginBottom: 12,
                          color: "#262626",
                          fontSize: 18,
                          fontWeight: 600,
                          marginTop: 0,
                        }}
                      >
                        {feature.title}
                      </h3>
                      <p style={{ color: "#8c8c8c", margin: 0, fontSize: 14 }}>
                        {feature.description}
                      </p>
                    </div>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        </div>

        {/* Tech Stack Section */}
        <div style={{ marginBottom: 80 }}>
          <Card
            style={{
              borderRadius: 12,
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              background: "#fff",
            }}
          >
            <Space
              direction="vertical"
              size="large"
              style={{ width: "100%" }}
              align="center"
            >
              <h3
                style={{
                  margin: 0,
                  color: "#262626",
                  fontSize: 24,
                  fontWeight: 600,
                  marginTop: 0,
                }}
              >
                技术栈
              </h3>
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: 16,
                  justifyContent: "center",
                }}
              >
                {techStack.map((tech, index) => (
                  <Tag
                    key={index}
                    color={tech.color}
                    style={{
                      fontSize: 16,
                      padding: "8px 20px",
                      borderRadius: 6,
                      marginBottom: 8,
                    }}
                  >
                    {tech.name}
                  </Tag>
                ))}
              </div>
            </Space>
          </Card>
        </div>

        {/* FastAPI Architecture Section */}
        <div style={{ marginBottom: 80 }}>
          <Card
            style={{
              borderRadius: 12,
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              background: "#fff",
            }}
            styles={{ body: { padding: "48px 32px" } }}
          >
            <Space direction="vertical" size="large" style={{ width: "100%" }}>
              <div style={{ textAlign: "center", marginBottom: 32 }}>
                <h2
                  style={{
                    fontSize: 32,
                    fontWeight: 600,
                    color: "#262626",
                    marginBottom: 16,
                    marginTop: 0,
                  }}
                >
                  <ApiOutlined style={{ marginRight: 12, color: "#1890ff" }} />
                  FastAPI 后端架构
                </h2>
                <p
                  style={{
                    fontSize: 16,
                    color: "#8c8c8c",
                    margin: 0,
                    maxWidth: 700,
                    margin: "0 auto",
                  }}
                >
                  采用现代化 Python Web 框架，构建高性能、类型安全的 RESTful API
                  服务
                </p>
              </div>

              <Divider style={{ margin: "32px 0" }} />

              <Row gutter={[32, 32]}>
                {fastapiFeatures.map((feature, index) => (
                  <Col xs={24} sm={12} lg={8} key={index}>
                    <Card
                      style={{
                        height: "100%",
                        borderRadius: 8,
                        border: "1px solid #f0f0f0",
                        boxShadow: "none",
                        transition: "all 0.3s",
                      }}
                      styles={{ body: { padding: 24 } }}
                      hoverable
                    >
                      <Space
                        direction="vertical"
                        size="small"
                        style={{ width: "100%" }}
                      >
                        <div>{feature.icon}</div>
                        <h3
                          style={{
                            fontSize: 18,
                            fontWeight: 600,
                            color: "#262626",
                            marginBottom: 12,
                            marginTop: 8,
                          }}
                        >
                          {feature.title}
                        </h3>
                        <p
                          style={{
                            fontSize: 14,
                            color: "#8c8c8c",
                            margin: 0,
                            lineHeight: "1.6",
                          }}
                        >
                          {feature.description}
                        </p>
                      </Space>
                    </Card>
                  </Col>
                ))}
              </Row>

              <Divider style={{ margin: "32px 0" }} />

              <div
                style={{
                  background:
                    "linear-gradient(135deg, #e6f7ff 0%, #f0f5ff 100%)",
                  borderRadius: 8,
                  padding: "24px 32px",
                  borderLeft: "4px solid #1890ff",
                }}
              >
                <Space
                  direction="vertical"
                  size="small"
                  style={{ width: "100%" }}
                >
                  <h4
                    style={{
                      fontSize: 16,
                      fontWeight: 600,
                      color: "#262626",
                      marginBottom: 8,
                      marginTop: 0,
                    }}
                  >
                    <CodeOutlined style={{ marginRight: 8 }} />
                    核心技术栈
                  </h4>
                  <div
                    style={{
                      display: "flex",
                      flexWrap: "wrap",
                      gap: 12,
                      marginTop: 8,
                    }}
                  >
                    <Tag
                      color="blue"
                      style={{
                        fontSize: 14,
                        padding: "6px 14px",
                        borderRadius: 4,
                      }}
                    >
                      Python 3.11+
                    </Tag>
                    <Tag
                      color="teal"
                      style={{
                        fontSize: 14,
                        padding: "6px 14px",
                        borderRadius: 4,
                      }}
                    >
                      FastAPI 0.127+
                    </Tag>
                    <Tag
                      color="orange"
                      style={{
                        fontSize: 14,
                        padding: "6px 14px",
                        borderRadius: 4,
                      }}
                    >
                      SQLModel
                    </Tag>
                    <Tag
                      color="green"
                      style={{
                        fontSize: 14,
                        padding: "6px 14px",
                        borderRadius: 4,
                      }}
                    >
                      aiosqlite
                    </Tag>
                    <Tag
                      color="purple"
                      style={{
                        fontSize: 14,
                        padding: "6px 14px",
                        borderRadius: 4,
                      }}
                    >
                      httpx
                    </Tag>
                    <Tag
                      color="cyan"
                      style={{
                        fontSize: 14,
                        padding: "6px 14px",
                        borderRadius: 4,
                      }}
                    >
                      loguru
                    </Tag>
                    <Tag
                      color="red"
                      style={{
                        fontSize: 14,
                        padding: "6px 14px",
                        borderRadius: 4,
                      }}
                    >
                      uv
                    </Tag>
                  </div>
                </Space>
              </div>
            </Space>
          </Card>
        </div>

        {/* Performance Comparison Section */}
        <div style={{ marginBottom: 80 }}>
          <h2
            style={{
              textAlign: "center",
              marginBottom: 48,
              color: "#262626",
              fontSize: 32,
              fontWeight: 600,
              marginTop: 0,
            }}
          >
            <ThunderboltOutlined
              style={{ marginRight: 12, color: "#f5222d" }}
            />
            性能对比
          </h2>
          <Card
            style={{
              borderRadius: 12,
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              background: "#fff",
            }}
            styles={{ body: { padding: "40px 32px" } }}
          >
            <Row gutter={[32, 32]}>
              <Col xs={24} md={8}>
                <Card
                  style={{
                    textAlign: "center",
                    borderRadius: 8,
                    border: "1px solid #f0f0f0",
                    boxShadow: "none",
                    height: "100%",
                  }}
                  styles={{ body: { padding: "32px 24px" } }}
                >
                  <Space
                    direction="vertical"
                    size="middle"
                    style={{ width: "100%" }}
                  >
                    <div
                      style={{
                        fontSize: 48,
                        fontWeight: 700,
                        color: "#52c41a",
                      }}
                    >
                      50x
                    </div>
                    <h3
                      style={{
                        fontSize: 18,
                        fontWeight: 600,
                        color: "#262626",
                        margin: 0,
                      }}
                    >
                      并发处理性能
                    </h3>
                    <p style={{ fontSize: 14, color: "#8c8c8c", margin: 0 }}>
                      Flask: 4 QPS → FastAPI: 200+ QPS
                    </p>
                  </Space>
                </Card>
              </Col>
              <Col xs={24} md={8}>
                <Card
                  style={{
                    textAlign: "center",
                    borderRadius: 8,
                    border: "1px solid #f0f0f0",
                    boxShadow: "none",
                    height: "100%",
                  }}
                  styles={{ body: { padding: "32px 24px" } }}
                >
                  <Space
                    direction="vertical"
                    size="middle"
                    style={{ width: "100%" }}
                  >
                    <div
                      style={{
                        fontSize: 48,
                        fontWeight: 700,
                        color: "#1890ff",
                      }}
                    >
                      2x
                    </div>
                    <h3
                      style={{
                        fontSize: 18,
                        fontWeight: 600,
                        color: "#262626",
                        margin: 0,
                      }}
                    >
                      响应速度
                    </h3>
                    <p style={{ fontSize: 14, color: "#8c8c8c", margin: 0 }}>
                      Flask: ~100ms → FastAPI: &lt;50ms
                    </p>
                  </Space>
                </Card>
              </Col>
              <Col xs={24} md={8}>
                <Card
                  style={{
                    textAlign: "center",
                    borderRadius: 8,
                    border: "1px solid #f0f0f0",
                    boxShadow: "none",
                    height: "100%",
                  }}
                  styles={{ body: { padding: "32px 24px" } }}
                >
                  <Space
                    direction="vertical"
                    size="middle"
                    style={{ width: "100%" }}
                  >
                    <div
                      style={{
                        fontSize: 48,
                        fontWeight: 700,
                        color: "#faad14",
                      }}
                    >
                      -40%
                    </div>
                    <h3
                      style={{
                        fontSize: 18,
                        fontWeight: 600,
                        color: "#262626",
                        margin: 0,
                      }}
                    >
                      代码量减少
                    </h3>
                    <p style={{ fontSize: 14, color: "#8c8c8c", margin: 0 }}>
                      更简洁的代码实现
                    </p>
                  </Space>
                </Card>
              </Col>
            </Row>
          </Card>
        </div>

        {/* Quick Links Section */}
        <div style={{ marginBottom: 80 }}>
          <h2
            style={{
              textAlign: "center",
              marginBottom: 48,
              color: "#262626",
              fontSize: 32,
              fontWeight: 600,
              marginTop: 0,
            }}
          >
            快速导航
          </h2>
          <Row gutter={[24, 24]}>
            {quickLinks.map((link, index) => (
              <Col xs={24} sm={12} lg={6} key={index}>
                <Link href={link.href}>
                  <Card
                    hoverable
                    style={{
                      height: "100%",
                      borderRadius: 12,
                      boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                      textAlign: "center",
                      transition: "all 0.3s",
                    }}
                    styles={{ body: { padding: "32px 16px" } }}
                  >
                    <Space
                      direction="vertical"
                      size="middle"
                      style={{ width: "100%" }}
                    >
                      <div style={{ fontSize: 40, color: "#1890ff" }}>
                        {link.icon}
                      </div>
                      <h3
                        style={{
                          margin: 0,
                          color: "#262626",
                          fontSize: 18,
                          fontWeight: 600,
                          marginTop: 0,
                        }}
                      >
                        {link.title}
                      </h3>
                      <ArrowRightOutlined
                        style={{ color: "#1890ff", fontSize: 20 }}
                      />
                    </Space>
                  </Card>
                </Link>
              </Col>
            ))}
          </Row>
        </div>

        {/* CTA Section */}
        <Card
          style={{
            borderRadius: 12,
            background: "linear-gradient(135deg, #1890ff 0%, #096dd9 100%)",
            border: "none",
            textAlign: "center",
            padding: "40px 20px",
          }}
        >
          <Space direction="vertical" size="large" style={{ width: "100%" }}>
            <h3
              style={{
                color: "#fff",
                margin: 0,
                fontSize: 24,
                fontWeight: 600,
                marginTop: 0,
              }}
            >
              准备好了吗？
            </h3>
            <p
              style={{
                color: "rgba(255,255,255,0.9)",
                fontSize: 16,
                margin: 0,
              }}
            >
              立即开始使用 OCS 题库系统，体验智能化的考试管理
            </p>
            <div>
              <CheckCircleOutlined
                style={{ fontSize: 32, color: "#fff", marginRight: 16 }}
              />
              <CheckCircleOutlined
                style={{ fontSize: 32, color: "#fff", marginRight: 16 }}
              />
              <CheckCircleOutlined style={{ fontSize: 32, color: "#fff" }} />
            </div>
          </Space>
        </Card>

        {/* Author & Acknowledgments Section */}
        <Card
          style={{
            borderRadius: 12,
            background: "#fff",
            boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            marginBottom: 60,
          }}
          styles={{ body: { padding: "32px 40px" } }}
        >
          <Row gutter={[32, 32]}>
            <Col xs={24} md={12}>
              <Space
                direction="vertical"
                size="small"
                style={{ width: "100%" }}
              >
                <h3
                  style={{
                    fontSize: 18,
                    fontWeight: 600,
                    color: "#262626",
                    marginBottom: 16,
                    marginTop: 0,
                  }}
                >
                  <SafetyOutlined style={{ marginRight: 8 }} />
                  作者
                </h3>
                <div>
                  <p
                    style={{
                      fontSize: 16,
                      fontWeight: 600,
                      color: "#262626",
                      margin: "0 0 8px 0",
                    }}
                  >
                    Chiway Wang
                  </p>
                  <Space direction="vertical" size="small">
                    <a
                      href="mailto:wchiway@163.com"
                      style={{
                        color: "#1890ff",
                        textDecoration: "none",
                        fontSize: 14,
                      }}
                    >
                      📧 wchiway@163.com
                    </a>
                    <a
                      href="https://chiway.blog"
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: "#1890ff",
                        textDecoration: "none",
                        fontSize: 14,
                      }}
                    >
                      🌐 chiway.blog
                    </a>
                  </Space>
                </div>
              </Space>
            </Col>
            <Col xs={24} md={12}>
              <Space
                direction="vertical"
                size="small"
                style={{ width: "100%" }}
              >
                <h3
                  style={{
                    fontSize: 18,
                    fontWeight: 600,
                    color: "#262626",
                    marginBottom: 16,
                    marginTop: 0,
                  }}
                >
                  <CheckCircleOutlined style={{ marginRight: 8 }} />
                  致谢
                </h3>
                <p
                  style={{
                    fontSize: 14,
                    color: "#8c8c8c",
                    margin: 0,
                    lineHeight: "1.8",
                  }}
                >
                  感谢以下开源项目的支持：
                </p>
                <div
                  style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: 8,
                    marginTop: 8,
                  }}
                >
                  <Tag color="teal">FastAPI</Tag>
                  <Tag color="orange">SQLModel</Tag>
                  <Tag color="red">uv</Tag>
                  <Tag color="blue">Next.js</Tag>
                  <Tag color="cyan">Ant Design</Tag>
                </div>
                <p
                  style={{
                    fontSize: 14,
                    color: "#8c8c8c",
                    margin: "8px 0 0 0",
                  }}
                >
                  原项目：ai-ocs-question_bank by Miaozeqiu
                </p>
              </Space>
            </Col>
          </Row>
        </Card>

        {/* Footer */}
        <div
          style={{
            textAlign: "center",
            marginTop: 60,
            padding: "20px 0",
            borderTop: "1px solid #e8e8e8",
          }}
        >
          <span style={{ color: "#8c8c8c", fontSize: 14 }}>
            © 2024 OCS 题库系统 · 基于 MIT 许可证开源
          </span>
        </div>
      </div>
    </div>
  );
}
