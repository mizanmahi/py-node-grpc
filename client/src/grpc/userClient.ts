import { loadProto } from './loader';
import * as path from 'path';

const USER_PROTO_PATH = path.join(
   __dirname,
   '..',
   '..',
   '..',
   'protos',
   'user.proto'
);
const userProto = loadProto(USER_PROTO_PATH);
export const UserService = (userProto as any).users.UserService;
export const userClient = new UserService(
   'localhost:50051',
   require('@grpc/grpc-js').credentials.createInsecure()
);
