import { Settings as LayoutSettings } from '@ant-design/pro-components';

const Settings: LayoutSettings & {
  pwa?: boolean;
  logo?: string;
} = {
  navTheme: 'light',
  // 拂晓蓝
  primaryColor: '#1890ff',
  layout: 'top',
  contentWidth: 'Fixed',
  headerHeight: 48,
  fixedHeader: false,
  fixSiderbar: true,
  colorWeak: false,
  title: 'Fleece Admin',
  splitMenus: false,
  footerRender: false,
  pwa: false,
  logo: 'https://avatars.githubusercontent.com/u/101970052?s=200&v=4',
  iconfontUrl: '',
};

export default Settings;
