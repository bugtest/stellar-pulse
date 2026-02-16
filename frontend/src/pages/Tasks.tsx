import { useState, useEffect } from 'react'
import { Card, Table, Button, Modal, Form, Input, Select, Switch, Space, Tag, message } from 'antd'
import { PlusOutlined, PlayCircleOutlined, ReloadOutlined } from '@ant-design/icons'
import { getTasks, createTask, deleteTask, runTask } from '../api'

const Tasks: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [tasks, setTasks] = useState<any[]>([])
  const [modalVisible, setModalVisible] = useState(false)
  const [form] = Form.useForm()

  const loadData = async () => {
    setLoading(true)
    try {
      const data = await getTasks()
      setTasks((data as any[]) || [])
    } catch (error) {
      console.error('Failed to load tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleCreateTask = async (values: any) => {
    try {
      await createTask(values)
      message.success('任务创建成功')
      setModalVisible(false)
      form.resetFields()
      loadData()
    } catch (error) {
      message.error('创建失败')
    }
  }

  const handleRunTask = async (taskId: number) => {
    try {
      await runTask(taskId)
      message.success('任务已触发执行')
      loadData()
    } catch (error) {
      message.error('执行失败')
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    try {
      await deleteTask(taskId)
      message.success('任务已删除')
      loadData()
    } catch (error) {
      message.error('删除失败')
    }
  }

  const columns = [
    { title: '任务名称', dataIndex: 'name', key: 'name' },
    { title: '类型', dataIndex: 'task_type', key: 'task_type' },
    { title: '调度方式', dataIndex: 'schedule_type', key: 'schedule_type', render: (v: string) => {
      const map: any = { manual: '手动', cron: 'Cron', interval: '间隔' }
      return map[v] || v
    }},
    { title: '启用', dataIndex: 'enabled', key: 'enabled', render: (v: boolean) => v ? '是' : '否' },
    { title: '上次状态', dataIndex: 'last_status', key: 'last_status', render: (v: string) => {
      const color = v === 'success' ? 'green' : v === 'failed' ? 'red' : 'default'
      return <Tag color={color}>{v || '-'}</Tag>
    }},
    { title: '上次运行', dataIndex: 'last_run_at', key: 'last_run_at', render: (v: string) => v ? new Date(v).toLocaleString() : '-' },
    { title: '操作', key: 'action', render: (_: any, record: any) => (
      <Space>
        <Button size="small" type="link" icon={<PlayCircleOutlined />} onClick={() => handleRunTask(record.id)}>
          执行
        </Button>
        <Button size="small" danger type="link" onClick={() => handleDeleteTask(record.id)}>
          删除
        </Button>
      </Space>
    )},
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ margin: 0 }}>任务中心</h2>
        <Space>
          <Button icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
            创建任务
          </Button>
          <Button icon={<ReloadOutlined />} onClick={loadData}>
            刷新
          </Button>
        </Space>
      </div>

      <Card>
        <Table
          dataSource={tasks}
          columns={columns}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="创建任务"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
        width={700}
      >
        <Form form={form} layout="vertical" onFinish={handleCreateTask}>
          <Form.Item name="name" label="任务名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea rows={2} />
          </Form.Item>
          <Form.Item name="task_type" label="任务类型" rules={[{ required: true }]} initialValue="script">
            <Select>
              <Select.Option value="script">脚本</Select.Option>
              <Select.Option value="command">命令</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="script_type" label="脚本类型" initialValue="bash">
            <Select>
              <Select.Option value="bash">Bash</Select.Option>
              <Select.Option value="python">Python</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="script" label="脚本内容" rules={[{ required: true }]}>
            <Input.TextArea rows={6} placeholder="#!/bin/bash\necho 'Hello World'" />
          </Form.Item>
          <Form.Item name="schedule_type" label="调度方式" initialValue="manual">
            <Select>
              <Select.Option value="manual">手动执行</Select.Option>
              <Select.Option value="cron">Cron表达式</Select.Option>
              <Select.Option value="interval">间隔执行</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="cron_expression" label="Cron表达式">
            <Input placeholder="0 * * * *" />
          </Form.Item>
          <Form.Item name="timeout" label="超时时间(秒)" initialValue={300}>
            <Input type="number" />
          </Form.Item>
          <Form.Item name="enabled" label="启用" valuePropName="checked" initialValue={true}>
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Tasks
