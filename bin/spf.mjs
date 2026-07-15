#!/usr/bin/env node

import { execSync } from 'child_process';

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(`secure-planning-framework - Security rules engine for AI-assisted development

Usage:
  npx spf                       # show this help
  npx spf audit                 # run framework audit
  npx spf activate              # activate framework for current task
  npx spf query "<rule>"        # query specific rule
  npx spf graph                 # run graphify on framework

Options:
  --help, -h                    # show help
  --version, -v                 # show version
  --json                        # output as JSON
  --verbose, -V                 # verbose output

Examples:
  npx spf audit
  npx spf activate
  npx spf query "COM-002"
  npx spf graph .
`);
    process.exit(0);
  }
  
  if (args[0] === '--version' || args[0] === '-v') {
    console.log('1.0.0');
    process.exit(0);
  }
  
  // Run the appropriate command
  const command = args.join(' ');
  console.log(`Running: spf ${command}\n`);
  
  try {
    execSync(`python3 scripts/framework_runner.py ${command}`, { stdio: 'inherit' });
  } catch (err) {
    console.error(`❌ Command failed: ${command}`);
    process.exit(err.status || 1);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
