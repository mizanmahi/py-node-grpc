import { loadProto } from './loader';
import * as path from 'path';

const AGENT_PROTO_PATH = path.join(
   __dirname,
   '..',
   '..',
   '..',
   'protos',
   'agent.proto'
);
const agentProto = loadProto(AGENT_PROTO_PATH);
export const AgentService = (agentProto as any).agent.AgentService;
export const agentClient = new AgentService(
   'localhost:50051',
   require('@grpc/grpc-js').credentials.createInsecure()
);
