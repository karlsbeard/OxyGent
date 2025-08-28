import { useAppStore } from '@/shared/stores/appStore';
import type { Agent } from '@/shared/types';
import type { FC } from 'react';
import { useEffect, useState } from 'react';
import { AgentNode } from './AgentNode';

export const AgentTree: FC = () => {
  const { agents, agentIdDict, isLoadingAgents } = useAppStore();
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set());

  // Auto-expand root nodes
  useEffect(() => {
    if (agents.length > 0) {
      const rootAgents = agents.filter((agent) => !agent.path || agent.path.length <= 1);
      setExpandedNodes(new Set(rootAgents.map((agent) => agent.id)));
    }
  }, [agents]);

  const toggleNode = (nodeId: string) => {
    setExpandedNodes((prev) => {
      const next = new Set(prev);
      if (next.has(nodeId)) {
        next.delete(nodeId);
      } else {
        next.add(nodeId);
      }
      return next;
    });
  };

  const buildTree = (agents: Agent[]): Agent[] => {
    const nodeMap = new Map<string, Agent>();
    const tree: Agent[] = [];

    // Create node map
    agents.forEach((agent) => {
      nodeMap.set(agent.id, { ...agent, children: [] });
    });

    // Build tree structure
    agents.forEach((agent) => {
      if (!agent.path || agent.path.length <= 1) {
        // Root node
        const node = nodeMap.get(agent.id);
        if (node) tree.push(node);
      } else {
        // Child node - find parent
        const parentPath = agent.path.slice(0, -1);
        const parentId = parentPath[parentPath.length - 1];
        const parent = nodeMap.get(parentId);
        const child = nodeMap.get(agent.id);

        if (parent && child) {
          if (!parent.children) parent.children = [];
          parent.children.push(child);
        }
      }
    });

    return tree;
  };

  const renderTree = (nodes: Agent[], level = 0): React.ReactNode => {
    return nodes.map((node) => (
      <div key={node.id} className={`${level > 0 ? 'ml-6' : ''}`}>
        <AgentNode
          agent={node}
          agentIdDict={agentIdDict}
          isExpanded={expandedNodes.has(node.id)}
          onToggle={() => toggleNode(node.id)}
          level={level}
        />

        {/* Render children if expanded */}
        {node.children && node.children.length > 0 && expandedNodes.has(node.id) && (
          <div className="mt-2">{renderTree(node.children, level + 1)}</div>
        )}
      </div>
    ));
  };

  if (isLoadingAgents) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (agents.length === 0) {
    return (
      <div className="flex items-center justify-center h-32 text-gray-500">
        <div className="text-center">
          <svg
            className="w-12 h-12 mx-auto mb-2 text-gray-300"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
            />
          </svg>
          <p>No agents available</p>
        </div>
      </div>
    );
  }

  const treeData = buildTree(agents);

  return <div className="p-2 space-y-2 overflow-auto h-full">{renderTree(treeData)}</div>;
};
