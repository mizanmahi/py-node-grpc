import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
// import * as path from 'path';

export function loadProto(protoFile: string) {
   const packageDef = protoLoader.loadSync(protoFile, {
      keepCase: true,
      longs: String,
      enums: String,
      defaults: true,
      oneofs: true,
   });
   return grpc.loadPackageDefinition(packageDef);
}
