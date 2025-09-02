import { userClient } from '../grpc/userClient';

export function getUser(user_id: string): Promise<any> {
   return new Promise((resolve, reject) => {
      userClient.GetUser({ user_id }, (err: any, response: any) => {
         if (err) reject(err);
         else resolve(response);
      });
   });
}
