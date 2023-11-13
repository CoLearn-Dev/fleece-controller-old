import { PageContainer } from '@ant-design/pro-components';
import { Card } from 'antd';
import React from 'react';

const Home: React.FC = () => {
  return (
    <div>
      <Card>
        <h1> Welcome to Fleece Admin Page! </h1>
        TODO: explain the project
      </Card>
      <Card>TODO: provide some action items: check GH, run live demo, etc.</Card>
      <Card>
        TODO: configure and monitor service liveness: controller, worker number, simulator used or
        not, etc.
      </Card>
      <Card>TODO: Provide a live chatbot served by controller</Card>
    </div>
  );
};

export default Home;
