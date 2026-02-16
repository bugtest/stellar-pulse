import { useState, useEffect } from 'react'
import { Card, Table, Tag, Button, Modal, Form, Input, Select, Switch, Space, message } from 'antd'
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons'
import { getAlerts, getAlertRules, createAlertRule, deleteAlertRule, acknowledgeAlert } from '../api'

const Alerts: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [alerts, setAlerts] = useState<any[]>([])
  const [rules, setRules] = useState<any[]>([])
  const [ruleModalVisible, setRuleModalVisible] = useState(false)
  const [form] = Form.useForm()

  const loadData = async () => {
    setLoading(true)
    try {
      const [alertsData, rulesData] = await Promise.all([
        getAlerts(),
        getAlertRules()
      ])
      setAlerts(alertsData.data || [])
      setRules(rulesData.data || [])
    } catch (error) {
      console.error('Failed to load alerts:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleAcknowledge = async (alertId: number) => {
    try {
      await acknowledgeAlert(alertId, { acknowledged_by: 'admin' })
      message.success('告警已确认')
      loadData()
    } catch (error) {
      message.error('操作失败')
    }
  }

  const handleCreateRule = async (values: any) => {
    try {
      await createAlertRule(values)
      message.success('规则创建成功')
      setRuleModalVisible(false)
      form.resetFields()
      loadData()
    } catch (error) {
      message.error('创建失败')
    }
  }

  const handleDeleteRule = async (ruleId: number) => {
    try {
      await deleteAlertRule(ruleId)
      message.success('规则已删除')
      loadData()
    } catch (error) {
      message.error('删除失败')
    }
  }

  const alertColumns = [
    { title: '告警标题', dataIndex: 'title', key: 'title' },
    { title: '严重程度', dataIndex: 'severity', key: 'severity', render: (sev: string) => {
      const color = sev === 'critical' ? 'red' : sev === 'warning' ? 'orange' : 'blue'
      return <Tag color={color}>{sev}</Tag>
    }},
    { title: '状态', dataIndex: 'status', key: 'status', render: (status: string) => {
      const color = status === 'firing' ? 'red' : status === 'acknowledged' ? 'orange' : 'green'
      return <Tag color={color}>{status}</Tag>
    }},
    { title: '目标', dataIndex: 'target_name', key: 'target_name' },
    { title: '时间', dataIndex: 'created_at', key: 'created_at', render: (v: string) => v ? new Date(v).toLocaleString() : '-' },
    { title: '操作', key: 'action', render: (_: any, record: any) => (
      record.status === 'firing' && (
        <Button size="small" type="link" onClick={() => handleAcknowledge(record.id)}>
          确认
        </Button>
      )
    )},
  ]

  const ruleColumns = [
    { title: '规则名称', dataIndex: 'name', key: 'name' },
    { title: '指标', dataIndex: 'metric_name', key: 'metric_name' },
    { title: '条件', dataIndex: 'condition', key: 'condition', render: (cond: string, row: any) => `${cond} ${row.threshold}` },
    { title: '严重程度', dataIndex: 'severity', key: 'severity' },
    { title: '启用', dataIndex: 'enabled', key: 'enabled', render: (v: boolean) => v ? '是' : '否' },
    { title: '操作', key: 'action', render: (_: any, record: any) => (
      <Button size="small" danger type="link" onClick={() => handleDeleteRule(record.id)}>
        删除
      </Button>
    )},
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ margin: 0 }}>告警管理</h2>
        <Space>
          <Button icon={<PlusOutlined />} onClick={() => setRuleModalVisible(true)}>
            创建规则
          </Button>
          <Button icon={<ReloadOutlined />} onClick={loadData}>
            刷新
          </Button>
        </Space>
      </div>

      <Card title="告警列表" style={{ marginBottom: 16 }}>
        <Table
          dataSource={alerts}
          columns={alertColumns}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Card title="告警规则">
        <Table
          dataSource={rules}
          columns={ruleColumns}
          rowKey="id"
          loading={loading}
          pagination={false}
        />
      </Card>

      <Modal
        title="创建告警规则"
        open={ruleModalVisible}
        onCancel={() => setRuleModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleCreateRule}>
          <Form.Item name="name" label="规则名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="metric_name" label="指标名称" rules={[{ required: true }]}>
            <Select>
              <Select.Option value="cpu">CPU使用率</Select.Option>
              <Select.Option value="memory">内存使用率</Select.Option>
              <Select.Option value="pod_status">Pod状态</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="condition" label="条件" rules={[{ required: true }]}>
            <Select>
              <Select.Option value="gt">大于</Select.Option>
              <Select.Option value="lt">小于</Select.Option>
              <Select.Option value="gte">大于等于</Select.Option>
              <Select.Option value="lte">小于等于</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="threshold" label="阈值" rules={[{ required: true }]}>
            <Input type="number" />
          </Form.Item>
          <Form.Item name="severity" label="严重程度" initialValue="warning">
            <Select>
              <Select.Option value="critical">Critical</Select.Option>
              <Select.Option value="warning">Warning</Select.Option>
              <Select.Option value="info">Info</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="enabled" label="启用" valuePropName="checked" initialValue={true}>
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Alerts
