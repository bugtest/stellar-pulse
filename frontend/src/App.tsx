import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout, Menu } from 'antd'
import {
  DashboardOutlined,
  AlertOutlined,
  RocketOutlined,
  BookOutlined,
  MessageOutlined,
  SettingOutlined,
} from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'

import Dashboard from './pages/Dashboard'
import Alerts from './pages/Alerts'
import Tasks from './pages/Tasks'
import Knowledge from './pages/Knowledge'
import Chat from './pages/Chat'
import Settings from './pages/Settings'

const { Header, Content, Sider } = Layout

const App: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    { key: '/', icon: <DashboardOutlined />, label: '监控中心' },
    { key: '/alerts', icon: <AlertOutlined />, label: '告警管理' },
    { key: '/tasks', icon: <RocketOutlined />, label: '任务中心' },
    { key: '/knowledge', icon: <BookOutlined />, label: '知识库' },
    { key: '/chat', icon: <MessageOutlined />, label: 'AI 对话' },
    { key: '/settings', icon: <SettingOutlined />, label: '系统设置' },
  ]

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#001529', padding: '0 24px', display: 'flex', alignItems: 'center' }}>
        <div style={{ color: '#fff', fontSize: 20, fontWeight: 'bold', marginRight: 40 }}>
          StellarPulse
        </div>
      </Header>
      <Layout>
        <Sider width={200} style={{ background: '#fff' }}>
          <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            style={{ height: '100%', borderRight: 0 }}
            items={menuItems}
            onClick={({ key }) => navigate(key)}
          />
        </Sider>
        <Layout style={{ padding: '24px' }}>
          <Content style={{ background: '#fff', padding: 24, margin: 0, minHeight: 280 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/tasks" element={<Tasks />} />
              <Route path="/knowledge" element={<Knowledge />} />
              <Route path="/chat" element={<Chat />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </Layout>
  )
}

export default App
