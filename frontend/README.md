# OxyGent Web Interface / OxyGent Web界面

[English](#english) | [中文](#中文)

---

## English

### Overview

This is the modern web interface for **OxyGent**, a powerful multi-agent AI system. Built with Modern.js, React, and TypeScript, it provides an intuitive dashboard for managing and interacting with AI agents in real-time.

### 🚀 Features

- **Real-time Multi-Agent Management** - Monitor and control multiple AI agents simultaneously
- **Interactive Chat Interface** - Communicate with agents through a modern chat interface
- **Agent Tree Visualization** - Visual representation of agent hierarchies and relationships  
- **File Upload Support** - Drag-and-drop file upload with preview functionality
- **Node Detail Views** - Detailed inspection of individual agent nodes and their configurations
- **Responsive Design** - Works seamlessly across desktop and mobile devices
- **Real-time Updates** - Live status updates via WebSocket connections

### 🛠️ Tech Stack

- **Framework**: Modern.js 2.68+ (with Rsbuild for ultra-fast builds)
- **Frontend**: React 18 + TypeScript 5.7+
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand for client state, TanStack Query for server state
- **Real-time**: Socket.io for WebSocket communication
- **Build Tool**: Rsbuild (Rspack-based bundler)
- **Code Quality**: Biome for linting and formatting
- **Testing**: Vitest + React Testing Library

### 📋 Prerequisites

- **Node.js** 18.20.8+ (Node.js 22 LTS recommended)
- **pnpm** 8.0.0+
- **OxyGent Backend** running on port 8000

### 🏁 Quick Start

1. **Install pnpm (if not available)**
   ```bash
   npm install -g pnpm@9
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Start development server**
   ```bash
   pnpm dev
   ```
   Open http://localhost:8080 in your browser

4. **Build for production**
   ```bash
   pnpm build
   ```

### 🔧 Development Commands

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start development server |
| `pnpm build` | Build for production |
| `pnpm serve` | Preview production build |
| `pnpm lint` | Run linting and formatting |
| `pnpm lint:check` | Check code quality without auto-fix |
| `pnpm type-check` | Run TypeScript type checking |
| `pnpm test` | Run tests |
| `pnpm test:ui` | Run tests with UI |

### 📁 Project Structure

```
src/
├── features/              # Feature-first architecture
│   ├── chat/             # Chat interface components
│   │   └── components/   # ChatInterface, MessageBubble, etc.
│   ├── agents/           # Agent management
│   │   └── components/   # AgentTree, AgentNode, NodeDetail
│   └── dashboard/        # Main dashboard
│       └── components/   # Dashboard layout components
├── shared/               # Shared utilities
│   ├── components/       # Reusable UI components
│   ├── stores/          # Zustand state management
│   ├── providers/       # React context providers
│   ├── types/           # TypeScript definitions
│   └── utils/           # Utility functions
├── routes/              # Modern.js file-based routing
├── styles/             # Global styles
└── assets/            # Static assets
```

### ⚙️ Configuration

**Environment Variables** (create `.env` file):
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENABLE_DEBUG=false
```

**Key Config Files**:
- `modern.config.ts` - Modern.js configuration
- `tailwind.config.ts` - Tailwind CSS customization
- `biome.json` - Code linting and formatting rules
- `tsconfig.json` - TypeScript configuration

### 🔌 Backend Integration

The frontend connects to the OxyGent Python backend via:
- **REST API**: `/api/*` endpoints proxied to backend
- **WebSocket**: Real-time communication for live updates
- **File Upload**: Multipart form data for file attachments

Make sure the OxyGent backend is running on port 8000 before starting the frontend.

### 🐛 Troubleshooting

**Development server won't start?**
- Ensure Node.js 18.20.8+ is installed
- Clear node_modules: `pnpm reset && pnpm install`
- Check if port 8080 is available

**Type errors?**
- Run `pnpm type-check` to identify issues
- Ensure all imports use correct paths with `@/` alias

**Build fails?**
- Run `pnpm lint` to fix code style issues
- Check for missing dependencies

### 🤝 Contributing

1. Follow the existing code patterns and architecture
2. Use TypeScript for all new components
3. Run `pnpm lint` before committing
4. Add tests for new features
5. Update documentation as needed

---

## 中文

### 概述

这是 **OxyGent** 的现代化Web界面，OxyGent是一个强大的多智能体AI系统。基于Modern.js、React和TypeScript构建，提供直观的仪表板用于实时管理和与AI智能体交互。

### 🚀 功能特性

- **实时多智能体管理** - 同时监控和控制多个AI智能体
- **交互式聊天界面** - 通过现代化聊天界面与智能体交流
- **智能体树状可视化** - 智能体层次结构和关系的可视化展示
- **文件上传支持** - 支持拖放文件上传和预览功能
- **节点详情视图** - 详细检查单个智能体节点及其配置
- **响应式设计** - 在桌面和移动设备上无缝工作
- **实时更新** - 通过WebSocket连接实现实时状态更新

### 🛠️ 技术栈

- **框架**: Modern.js 2.68+ (使用Rsbuild实现超快构建)
- **前端**: React 18 + TypeScript 5.7+
- **样式**: Tailwind CSS 自定义设计系统
- **状态管理**: Zustand 管理客户端状态，TanStack Query 管理服务器状态
- **实时通信**: Socket.io WebSocket 通信
- **构建工具**: Rsbuild (基于Rspack的打包器)
- **代码质量**: Biome 代码检查和格式化
- **测试**: Vitest + React Testing Library

### 📋 环境要求

- **Node.js** 18.20.8+ (推荐使用 Node.js 22 LTS)
- **pnpm** 8.0.0+
- **OxyGent 后端** 运行在8000端口

### 🏁 快速开始

1. **安装 pnpm (如果尚未安装)**
   ```bash
   npm install -g pnpm@9
   ```

2. **安装依赖**
   ```bash
   pnpm install
   ```

3. **启动开发服务器**
   ```bash
   pnpm dev
   ```
   在浏览器中打开 http://localhost:8080

4. **构建生产版本**
   ```bash
   pnpm build
   ```

### 🔧 开发命令

| 命令 | 说明 |
|------|------|
| `pnpm dev` | 启动开发服务器 |
| `pnpm build` | 构建生产版本 |
| `pnpm serve` | 预览生产构建 |
| `pnpm lint` | 运行代码检查和格式化 |
| `pnpm lint:check` | 检查代码质量（不自动修复） |
| `pnpm type-check` | 运行TypeScript类型检查 |
| `pnpm test` | 运行测试 |
| `pnpm test:ui` | 运行测试（带UI界面） |

### 📁 项目结构

```
src/
├── features/              # 功能优先架构
│   ├── chat/             # 聊天界面组件
│   │   └── components/   # ChatInterface, MessageBubble等
│   ├── agents/           # 智能体管理
│   │   └── components/   # AgentTree, AgentNode, NodeDetail
│   └── dashboard/        # 主仪表板
│       └── components/   # 仪表板布局组件
├── shared/               # 共享工具
│   ├── components/       # 可复用UI组件
│   ├── stores/          # Zustand状态管理
│   ├── providers/       # React上下文提供程序
│   ├── types/           # TypeScript类型定义
│   └── utils/           # 工具函数
├── routes/              # Modern.js基于文件的路由
├── styles/             # 全局样式
└── assets/            # 静态资源
```

### ⚙️ 配置说明

**环境变量** (创建 `.env` 文件):
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENABLE_DEBUG=false
```

**关键配置文件**:
- `modern.config.ts` - Modern.js 配置
- `tailwind.config.ts` - Tailwind CSS 自定义配置
- `biome.json` - 代码检查和格式化规则
- `tsconfig.json` - TypeScript 配置

### 🔌 后端集成

前端通过以下方式连接到OxyGent Python后端：
- **REST API**: `/api/*` 端点代理到后端
- **WebSocket**: 实时通信用于实时更新
- **文件上传**: 多部分表单数据用于文件附件

在启动前端之前，请确保OxyGent后端在8000端口上运行。

### 🐛 故障排除

**开发服务器无法启动？**
- 确保已安装 Node.js 18.20.8+
- 清除 node_modules: `pnpm reset && pnpm install`
- 检查8080端口是否可用

**类型错误？**
- 运行 `pnpm type-check` 识别问题
- 确保所有导入使用正确的 `@/` 别名路径

**构建失败？**
- 运行 `pnpm lint` 修复代码风格问题
- 检查缺失的依赖项

### 🤝 参与贡献

1. 遵循现有的代码模式和架构
2. 对所有新组件使用TypeScript
3. 提交前运行 `pnpm lint`
4. 为新功能添加测试
5. 根据需要更新文档

---

### 📄 License / 许可证

This project is part of the OxyGent framework. Please refer to the main project license.

此项目是OxyGent框架的一部分，请参考主项目许可证。
