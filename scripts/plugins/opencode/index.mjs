export const ExpertPanelPlugin = async ({ client }) => {
  await client.app.log({
    body: {
      service: 'expert-panel',
      level: 'info',
      message: 'Expert Panel plugin loaded. Skills and subagents are installed separately by the verified installer.',
    },
  })

  return {
    'experimental.session.compacting': async (_input, output) => {
      output.context.push(`
## Expert Panel continuation capsule
Preserve only: GOAL, SCOPE, CONSTRAINTS, PROFILE, DECISIONS, EVIDENCE,
OPEN_CONFLICTS, COMPLETED, NEXT_ACTION, ROLLBACK, and FRESHNESS.
Do not preserve secrets, credentials, private prompts, or hidden reasoning.
`)
    },
  }
}
