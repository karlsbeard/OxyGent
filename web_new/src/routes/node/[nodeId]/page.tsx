import NodeDetail from '@/features/agents/components/NodeDetail';
import { Helmet } from '@modern-js/runtime/head';
import { useParams } from '@modern-js/runtime/router';

const NodeDetailPage = () => {
  return (
    <>
      <Helmet>
        <title>Node Detail - OxyGent</title>
      </Helmet>
      <NodeDetail />
    </>
  );
};

export default NodeDetailPage;
