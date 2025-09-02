import { getUser } from './services/userService';
import { runQuery } from './services/agentService';

async function main() {
   try {
      const user = await getUser('123');
      console.log('User:', user);

      const agentResponse = await runQuery('What is gRPC?');
      console.log('Agent Response:', agentResponse);
   } catch (err) {
      console.error('Error:', err);
   }
}

main();
