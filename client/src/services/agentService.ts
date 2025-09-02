import { agentClient } from '../grpc/agentClient';

export function runQuery(query: string): Promise<any> {
   return new Promise((resolve, reject) => {
      agentClient.RunQuery({ query }, (err: any, response: any) => {
         if (err) reject(err);
         else resolve(response);
      });
   });
}
