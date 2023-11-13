import { Card, Table, Tag, Space } from 'antd-v5';
import { CheckCircleOutlined } from '@ant-design/icons';
import ChatBox from '@/components/Chatbox';
import React from 'react';
import { useEffect, useState } from 'react';
import Cover from './fleece.png'

const Home: React.FC = () => {
  const [dataSource, setDataSource] = useState<Array<{ w_id: string, worker_url: string, created_at: string }>>([]);
  const [worker_err, setWorkerErr] = useState<string>('');
  useEffect(() => {
    let interval = setInterval(() => {
      const HTTP_TIMEOUT = 1000;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), HTTP_TIMEOUT);
      fetch('http://localhost:8000/list_workers', { signal: controller.signal }).then((res) => res.json()).then((data) => {
        setDataSource(data);
        setWorkerErr('[connected]');
      }).catch((e) => {
        console.log(e);
        setWorkerErr("[disconnected]");
      }).finally(() => {
        clearTimeout(timeoutId);
      });
    }
      , 500);
    return () => {
      clearInterval(interval);
    };
  }, []);
  return (
    <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
      <Card cover={
        <img src={Cover} alt="Fleece" style={{ height: 300, objectFit: "cover", objectPosition: "0 30%" }} />
      } style={{ width: "50%", marginLeft: "25%" }}>
        <h1> Welcome to <b style={{ color: '#FDB515' }}>Golden Fleece</b> Admin Page! </h1>
        Use this page to monitor Fleece network and interact with it.
      </Card>
      {/* <Card>TODO: provide some action items: check GH, run live demo, etc.</Card> */}
      <Card title="Interactive demo">
        <ChatBox />
      </Card>
      <Card title={
        <div>
          Worker monitoring <b style={worker_err.includes("dis")? { color: "red"} : { color: "green" }}>{worker_err}</b>
        </div>
      }>
        <Table dataSource={dataSource} columns={[
          {
            'title': 'Worker ID',
            'key': 'w_id',
            'dataIndex': 'w_id',
          },
          {
            'title': 'Worker URL',
            'key': 'worker_url',
            'dataIndex': 'worker_url',
            'render': (v) => {
              return (<Tag icon={<CheckCircleOutlined />} color="success">
                {v}
              </Tag>)
            }
          },
          {
            'title': 'Created At',
            'key': 'created_at',
            'dataIndex': 'created_at',
            'render': (v) => {
              // convert timestamp to date
              const date = new Date(v * 1000);
              return date.toLocaleString();
            },
            'sorter': (a, b) => a.created_at - b.created_at,
          },
        ]} />
      </Card>
    </Space>
  );
};

export default Home;
