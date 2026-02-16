import { useState, useEffect } from 'react'
import { Card, Table, Button, Modal, Form, Input, Space, Tag, message } from 'antd'
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons'
import { getArticles, getCases, createArticle, createCase, getCategories } from '../api'

const { TextArea } = Input

const Knowledge: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [articles, setArticles] = useState<any[]>([])
  const [cases, setCases] = useState<any[]>([])
  const [categories, setCategories] = useState<any[]>([])
  const [activeTab, setActiveTab] = useState('articles')
  const [modalVisible, setModalVisible] = useState(false)
  const [form] = Form.useForm()

  const loadData = async () => {
    setLoading(true)
    try {
      const [articlesData, casesData, categoriesData] = await Promise.all([
        getArticles(),
        getCases(),
        getCategories()
      ])
      setArticles((articlesData as any) || [])
      setCases((casesData as any) || [])
      setCategories((categoriesData as any) || [])
    } catch (error) {
      console.error('Failed to load knowledge:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleCreateArticle = async (values: any) => {
    try {
      await createArticle(values)
      message.success('文档创建成功')
      setModalVisible(false)
      form.resetFields()
      loadData()
    } catch (error) {
      message.error('创建失败')
    }
  }

  const handleCreateCase = async (values: any) => {
    try {
      await createCase(values)
      message.success('案例创建成功')
      setModalVisible(false)
      form.resetFields()
      loadData()
    } catch (error) {
      message.error('创建失败')
    }
  }

  const articleColumns = [
    { title: '标题', dataIndex: 'title', key: 'title' },
    { title: '作者', dataIndex: 'author', key: 'author' },
    { title: '标签', dataIndex: 'tags', key: 'tags', render: (v: string[]) => v?.map((t: string) => <Tag key={t}>{t}</Tag>) },
    { title: '浏览', dataIndex: 'views', key: 'views' },
    { title: '更新时间', dataIndex: 'updated_at', key: 'updated_at', render: (v: string) => v ? new Date(v).toLocaleString() : '-' },
  ]

  const caseColumns = [
    { title: '标题', dataIndex: 'title', key: 'title' },
    { title: '分类', dataIndex: 'category', key: 'category' },
    { title: '标签', dataIndex: 'tags', key: 'tags', render: (v: string[]) => v?.map((t: string) => <Tag key={t}>{t}</Tag>) },
    { title: '有用', dataIndex: 'helpful_count', key: 'helpful_count' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', render: (v: string) => v ? new Date(v).toLocaleString() : '-' },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ margin: 0 }}>知识库</h2>
        <Space>
          <Button icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
            新建
          </Button>
          <Button icon={<ReloadOutlined />} onClick={loadData}>
            刷新
          </Button>
        </Space>
      </div>

      <Card>
        <Table
          dataSource={activeTab === 'articles' ? articles : cases}
          columns={activeTab === 'articles' ? articleColumns : caseColumns}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={activeTab === 'articles' ? '创建文档' : '创建案例'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
        width={700}
      >
        <Form form={form} layout="vertical" onFinish={activeTab === 'articles' ? handleCreateArticle : handleCreateCase}>
          <Form.Item name="title" label="标题" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          {activeTab === 'articles' ? (
            <>
              <Form.Item name="content" label="内容" rules={[{ required: true }]}>
                <TextArea rows={10} />
              </Form.Item>
              <Form.Item name="author" label="作者">
                <Input />
              </Form.Item>
            </>
          ) : (
            <>
              <Form.Item name="problem" label="问题描述" rules={[{ required: true }]}>
                <TextArea rows={3} />
              </Form.Item>
              <Form.Item name="cause" label="原因分析">
                <TextArea rows={3} />
              </Form.Item>
              <Form.Item name="solution" label="解决方案">
                <TextArea rows={3} />
              </Form.Item>
              <Form.Item name="category" label="分类">
                <Input />
              </Form.Item>
            </>
          )}
        </Form>
      </Modal>
    </div>
  )
}

export default Knowledge
