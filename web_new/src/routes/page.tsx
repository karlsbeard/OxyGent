import Dashboard from '@/features/dashboard/components/Dashboard';
import { Helmet } from '@modern-js/runtime/head';

const Index = () => (
  <>
    <Helmet>
      <title>OxyGent - Multi-Agent AI System</title>
      <link rel="icon" type="image/x-icon" href="/image/group-favicon.png" />
    </Helmet>
    <Dashboard />
  </>
);

export default Index;
