export default [
  {
    path: '/user',
    layout: false,
    routes: [
      { name: 'Login', path: '/user/login', component: './user/Login' },
      { component: './404' },
    ],
  },
  { path: '/', redirect: '/home' },
  { path: '/home', name: 'Home', icon: 'crown', component: './Home' },
  { path: '/controller', name: 'Controller', icon: 'cluster', component: './Controller' },
  { path: '/worker', name: 'Worker', icon: 'desktop' },
  { path: '/simulator', name: 'Simulator', icon: 'experiment' },
  {
    path: 'https://llm-speedtest.colearn.cloud/',
    name: 'Speed Test',
    icon: 'dashboard',
    target: '_blank',
  },
  { component: './404' },
];
