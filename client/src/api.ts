import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import * as path from 'path';

// Path to your proto file
const USER_PROTO_PATH = path.join(
   __dirname,
   '..',
   '..',
   'protos',
   'user.proto'
);
console.log('Resolved USER_PROTO_PATH:', USER_PROTO_PATH);

// Load the proto definition
const packageDefinition = protoLoader.loadSync(USER_PROTO_PATH, {
   keepCase: true,
   longs: String,
   enums: String,
   defaults: true,
   oneofs: true,
});

const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
const userService = (protoDescriptor as any).users.UserService;

const client = new userService(
   'localhost:50051', // Change if your server runs elsewhere
   grpc.credentials.createInsecure()
);

// Replace 'yourMethod' with your RPC method name and adjust params
client.GetUser({ user_id: '123' }, (err: grpc.ServiceError, response: any) => {
   if (err) {
      console.error('gRPC Error:', err);
   } else {
      console.log('gRPC Response:', response);
   }
});
