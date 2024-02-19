import { outLogin } from '@/services/ant-design-pro/api';
import { LoginOutlined, LogoutOutlined, SettingOutlined, UserOutlined, WalletOutlined } from '@ant-design/icons';
import { Avatar, Menu, Spin } from 'antd';
import type { ItemType } from 'antd/lib/menu/hooks/useItems';
import { stringify } from 'querystring';
import type { MenuInfo } from 'rc-menu/lib/interface';
import React, { useCallback } from 'react';
import { history, useModel } from 'umi';
import HeaderDropdown from '../HeaderDropdown';
import styles from './index.less';

export type GlobalHeaderRightProps = {
  menu?: boolean;
};

const AvatarDropdown: React.FC<GlobalHeaderRightProps> = ({ menu }) => {
  const { initialState, setInitialState } = useModel('@@initialState');

  const onMenuClick = useCallback(
    (event: MenuInfo) => {
      const { key } = event;
      if (key === 'login') {
        const url = "https://serving-api.colearn.cloud:8443/oauth?code=test@colearn.dev";
        window.location.href = url;
        return;
      }
      if (key === 'logout') {
        localStorage.removeItem('token');
        setInitialState((s) => ({ ...s, currentUser: {
          email: 'Guest',
          avatar: '/icons8-who-100.png',
        } }));
        window.location.reload();
        return;
      }
      history.push(`/account/${key}`);
    },
    [setInitialState],
  );

  const loading = (
    <span className={`${styles.action} ${styles.account}`}>
      <Spin
        size="small"
        style={{
          marginLeft: 8,
          marginRight: 8,
        }}
      />
    </span>
  );

  if (!initialState) {
    return loading;
  }

  const { currentUser } = initialState;

  if (!currentUser || !currentUser.email) {
    console.log(currentUser);
    return loading;
  }

  const menuItems: ItemType[] = [
    ...(menu
      ? [
          {
            key: 'center',
            icon: <UserOutlined />,
            label: '个人中心',
          },
          {
            key: 'settings',
            icon: <SettingOutlined />,
            label: '个人设置',
          },
          {
            type: 'divider' as const,
          },
        ]
      : []),
    ...(currentUser.email == "Guest" ? [
      {
        key: 'login',
        icon: <LoginOutlined />,
        label: 'Login',
      },
    ] : []),
    {
      key: 'credit',
      icon: <WalletOutlined />,
      label: 'My Credit',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
    },
  ];

  const menuHeaderDropdown = (
    <Menu className={styles.menu} selectedKeys={[]} onClick={onMenuClick} items={menuItems} />
  );

  return (
    <HeaderDropdown overlay={menuHeaderDropdown}>
      <span className={`${styles.action} ${styles.account}`}>
        <Avatar size="small" className={styles.avatar} src={currentUser.avatar} alt="avatar" />
        <span className={`${styles.name} anticon`}>{currentUser.email ? currentUser.email : currentUser.name }</span>
      </span>
    </HeaderDropdown>
  );
};

export default AvatarDropdown;
