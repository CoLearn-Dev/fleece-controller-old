import { Badge, Card, Col, Descriptions, Divider, Progress, Row } from 'antd-v5';
import React from 'react';
import ChatBox from '@/components/Chatbox';
import Circuit from '@/components/Circuit';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { a11yLight, a11yDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { history, useModel } from 'umi';
import { useEffect, useState } from 'react';

const Playground: React.FC = () => {
  const [credit, setCredit] = useState<number>(0);
  const [chatId, setChatId] = useState<string>('');

  const { initialState, setInitialState } = useModel('@@initialState');
  const { currentUser } = initialState;

  const api_key = currentUser.api_token
    ? currentUser.api_token
    : '<Please login first to get API token>';
  const credit_api_url = 'https://serving-api.colearn.cloud:8443/get_remaining_credit';
  if (currentUser.api_token) {
    fetch(credit_api_url, { headers: { 'api-token': currentUser.api_token } })
      .then((response) => response.json())
      .then((data) => {
        setCredit(data.remaining_credit);
      });
  }

  const api_endpoint = 'https://serving-api.colearn.cloud:9000/v1';
  const bashCodeString =
    `\
curl ` +
    api_endpoint +
    `/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer ` +
    api_key +
    `" \\
  -d '{
    "model": "llama-2-7b-chat",
    "messages": [{"role": "user", "content": "Hello world!"}]
  }'\
   `;
  const pythonCodeString =
    `\
from openai import OpenAI

client = OpenAI(
    api_key="` +
    api_key +
    `",
    base_url="` +
    api_endpoint +
    `",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Hello world!",
        }
    ],
    model="llama-2-7b-chat",
)

print(chat_completion)\
  `;
  var api_items = [
    {
      key: '1',
      label: 'Your API key',
      children: api_key,
    },
    {
      key: '2',
      label: 'Your remaining credit',
      children: (
        <Progress
          percent={Math.min(Math.log(credit + 1) / Math.log(1.1), 100)}
          format={() => credit + ` fleece tokens`}
          size="small"
          style={{ width: 200 }}
          status="active"
          strokeColor={{ from: '#fd5315', to: '#FDB515' }}
        />
      ),
    },
    {
      key: '3',
      label: 'Service Status',
      span: 3,
      children: <Badge status="processing" text="Running" />,
    },
  ];
  var request_items = [
    {
      key: '1',
      label: 'Chat ID',
      children: chatId ? chatId : '...',
    },
  ];
  useEffect(() => {
    const chat_info_api_url = 'https://serving-api.colearn.cloud:8443/get_chat_info';
    fetch(chat_info_api_url, {
      headers: { 'api-token': currentUser.api_token, 'Content-Type': 'application/json' },
      method: 'POST',
      body: JSON.stringify({ chat_id: chatId }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
  }, [chatId]);

  return (
    <div>
      <Card>
        <h1>Try it out</h1>
        <p>
          We provide both
          <a style={{ color: '#FDB515' }}> API access </a>
          and
          <a style={{ color: '#FDB515' }}> Chatbox demo </a>
          for trying out our serving sytem.
        </p>
      </Card>
      <br />
      <Card>
        <h1>API access</h1>

        <Descriptions layout="vertical" bordered={true} items={api_items} />
        <Divider />
        <h3> Try it in your terminal: </h3>
        <SyntaxHighlighter language="bash" style={a11yDark}>
          {bashCodeString}
        </SyntaxHighlighter>
        <Divider />
        <h3>
          {' '}
          Try it with <a href="https://pypi.org/project/openai/">Python OpenAI package</a>:{' '}
        </h3>
        <SyntaxHighlighter language="python" style={a11yDark}>
          {pythonCodeString}
        </SyntaxHighlighter>
      </Card>

      <br />

      <Card>
        <h1> Chatbot demo </h1>
        <Row>
          <Col span={14}>
            <ChatBox setChatId={setChatId} />
          </Col>
          <Col span={1}></Col>
          <Col span={9}>
            <Card title="Serving details" bordered>
              <Descriptions layout="vertical" bordered={true} items={request_items} />
              <Divider />
              <Circuit chatId={chatId} />
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default Playground;