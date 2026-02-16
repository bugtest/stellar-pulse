import { Card, Form, Input, Button, Switch, message } from 'antd'

const Settings: React.FC = () => {
  // const [form] = Form.useForm()

  const handleSave = () => {
    message.success('设置已保存')
  }

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>系统设置</h2>

      <Card title="Kubernetes 配置" style={{ marginBottom: 16 }}>
        <Form layout="vertical">
          <Form.Item label="Kubeconfig 路径">
            <Input placeholder="~/.kube/config" />
          </Form.Item>
          <Form.Item label="刷新间隔(秒)">
            <Input type="number" placeholder="30" />
          </Form.Item>
        </Form>
      </Card>

      <Card title="Nanobot 配置" style={{ marginBottom: 16 }}>
        <Form layout="vertical">
          <Form.Item label="配置文件路径">
            <Input placeholder="~/.nanobot/config.json" />
          </Form.Item>
          <Form.Item label="工作空间路径">
            <Input placeholder="~/.nanobot/workspace" />
          </Form.Item>
        </Form>
      </Card>

      <Card title="告警通知" style={{ marginBottom: 16 }}>
        <Form layout="vertical">
          <Form.Item label="钉钉 Webhook">
            <Input placeholder="https://oapi.dingtalk.com/robot/send?access_token=xxx" />
          </Form.Item>
          <Form.Item label="企业微信 Webhook">
            <Input placeholder="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx" />
          </Form.Item>
          <Form.Item label="邮件通知">
            <Switch /> 启用邮件通知
          </Form.Item>
        </Form>
      </Card>

      <Card title="安全设置">
        <Form layout="vertical">
          <Form.Item label="API 密钥">
            <Input.Password placeholder="请输入API密钥" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" onClick={handleSave}>
              保存设置
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}

export default Settings
