import { useState, useEffect } from 'react'
import { Row, Col, Card, Statistic, Table, Tag, Spin } from 'antd'
import { ReloadOutlined } from '@ant-design/icons'
import { getOverview, getNodes, getPods, getDeployments } from '../api'

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [overview, setOverview] = useState<any>(null)
  const [nodes, setNodes] = useState<any[]>([])
  const [pods, setPods] = useState<any[]>([])
  const [deployments, setDeployments] = useState<any[]>([])

  const loadData = async () => {
    setLoading(true)
    try {
      const [overviewData, nodesData, podsData, deploymentsData] = await Promise.all([
        getOverview(),
        getNodes(),
        getPods(),
        getDeployments()
      ])
      setOverview(overviewData)
      setNodes((nodesData as any[]) || [])
      setPods((podsData as any[]) || [])
      setDeployments((deploymentsData as any[]) || [])
    } catch (error) {
      console.error('Failed to load data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000) // Refresh every 30s
    return () => clearInterval(interval)
  }, [])

  const nodeColumns = [
    { title: '节点', dataIndex: 'name', key: 'name' },
    { title: '状态', dataIndex: 'status', key: 'status', render: (status: string) => (
      <Tag color={status === 'Ready' ? 'green' : 'red'}>{status}</Tag>
    )},
    { title: 'CPU', dataIndex: 'cpu_cores', key: 'cpu_cores', render: (v: number) => `${v} 核` },
    { title: '内存', dataIndex: 'memory_bytes', key: 'memory', render: (v: number) => `${Math.round(v / 1024 / 1024 / 1024)} GB` },
    { title: 'Pod数', dataIndex: 'pods', key: 'pods' },
  ]

  const podColumns = [
    { title: 'Pod名称', dataIndex: 'name', key: 'name', ellipsis: true },
    { title: '命名空间', dataIndex: 'namespace', key: 'namespace' },
    { title: '状态', dataIndex: 'status', key: 'status', render: (status: string) => {
      const color = status === 'Running' ? 'green' : status === 'Pending' ? 'orange' : 'red'
      return <Tag color={color}>{status}</Tag>
    }},
    { title: '节点', dataIndex: 'node', key: 'node' },
    { title: '重启', dataIndex: 'restarts', key: 'restarts' },
    { title: '运行时间', dataIndex: 'age', key: 'age' },
  ]

  const deployColumns = [
    { title: '部署名称', dataIndex: 'name', key: 'name' },
    { title: '命名空间', dataIndex: 'namespace', key: 'namespace' },
    { title: '副本数', dataIndex: 'replicas', key: 'replicas' },
    { title: '就绪', dataIndex: 'ready_replicas', key: 'ready_replicas', render: (ready: number, row: any) => `${ready}/${row.replicas}` },
    { title: '可用', dataIndex: 'available_replicas', key: 'available_replicas' },
  ]

  if (loading && !overview) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    )
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ margin: 0 }}>监控中心</h2>
        <ReloadOutlined spin={loading} onClick={loadData} style={{ fontSize: 18, cursor: 'pointer' }} />
      </div>

      {/* Overview Stats */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic title="节点数" value={overview?.cluster?.nodes || 0} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Pod总数" value={overview?.cluster?.pods || 0} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="运行中" value={overview?.pods?.running || 0} valueStyle={{ color: '#3f8600' }} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="服务数" value={overview?.cluster?.services || 0} />
          </Card>
        </Col>
      </Row>

      {/* Resources */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card title="CPU cores">
            <Statistic title="总CPU" value={overview?.resources?.cpu_cores || 0} suffix="核" />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Memory">
            <Statistic title="总内存" value={overview?.resources?.memory_gb || 0} suffix="GB" />
          </Card>
        </Col>
      </Row>

      {/* Nodes Table */}
      <Card title="节点状态" style={{ marginBottom: 16 }}>
        <Table
          dataSource={nodes}
          columns={nodeColumns}
          rowKey="name"
          size="small"
          pagination={false}
        />
      </Card>

      {/* Deployments */}
      <Card title="部署状态" style={{ marginBottom: 16 }}>
        <Table
          dataSource={deployments}
          columns={deployColumns}
          rowKey="name"
          size="small"
          pagination={false}
        />
      </Card>

      {/* Pods Table */}
      <Card title="Pod状态">
        <Table
          dataSource={pods.slice(0, 20)}
          columns={podColumns}
          rowKey="name"
          size="small"
          pagination={{ pageSize: 20 }}
        />
      </Card>
    </div>
  )
}

export default Dashboard
