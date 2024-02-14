import { Settings as LayoutSettings } from '@ant-design/pro-components';

const Settings: LayoutSettings & {
  pwa?: boolean;
  logo?: string;
} = {
  navTheme: 'light',
  primaryColor: '#FDB515',
  layout: 'top',
  contentWidth: 'Fixed',
  headerHeight: 48,
  fixedHeader: false,
  fixSiderbar: true,
  colorWeak: false,
  title: 'FleeceServe',
  splitMenus: false,
  footerRender: false,
  pwa: false,
  logo: 'https://avatars.githubusercontent.com/u/101970052?s=200&v=4',
  iconfontUrl: '',
};

export default Settings;
