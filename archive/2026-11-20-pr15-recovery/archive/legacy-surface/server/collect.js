/* Compatibility launcher. Use one aggregate collector, never a raw event log.
 * See analytics/README.md for the required configuration and privacy gates. */
const { spawn } = require('node:child_process');
const path = require('node:path');
const child = spawn('python3', [path.resolve(__dirname, '../analytics/endpoint.py')], {stdio: 'inherit'});
for (const sig of ['SIGINT','SIGTERM']) process.on(sig, () => child.kill(sig));
child.on('error', () => { console.error('Python 3 is required.'); process.exitCode=1; });
child.on('exit', code => { process.exitCode=code ?? 1; });
