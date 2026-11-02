async (page) => {
  const base='http://127.0.0.1:18762/final-preview-v2/';
  const root='Coursework/prototype/tether-final-build/qa-shots/';
  const byName=name=>page.locator(`[data-label="${name}"]`).first();
  const click=async name=>{await byName(name).click();};
  const screenshot=async name=>page.screenshot({path:root+name+'.png',fullPage:true});
  await page.setViewportSize({width:430,height:932});
  await page.goto(base+'page_1.html');await page.waitForLoadState('load');await screenshot('01-desk');
  await click('hit_pause');await page.waitForURL('**/04_leave_a_thread.html*');await screenshot('02-save-empty');
  const where=page.locator('[data-label="where_stopped"] input');
  const next=page.locator('[data-label="next_move"] input');
  if((await where.getAttribute('maxlength'))!=='48'||(await next.getAttribute('maxlength'))!=='48') throw Error('Input length limit missing');
  await where.clear();await next.clear();await page.locator('[data-label="hit_save_with_variables"]').click();
  if(!await page.getByText('Add where you stopped first.').count()) throw Error('Missing first validation');
  await page.locator('[data-label="where_stopped"] input').fill('Stopped at the literature synthesis');
  await click('hit_save_with_variables');
  if(!await page.getByText('Add the next small move first.').count()) throw Error('Missing second validation');
  await page.locator('[data-label="next_move"] input').fill('Compare two studies');await screenshot('03-save-filled');
  await click('hit_save_with_variables');await page.waitForURL('**/05_ready_to_return.html*');await screenshot('04-saved');
  await click('hit_home');await page.waitForURL('**/page_1.html*');
  if(!await page.getByText('Stopped at the literature synthesis').count()) throw Error('Saved context not restored');
  if(!await page.getByText('Compare two studies').count()) throw Error('Saved action not restored');
  await screenshot('05-restored');await click('hit_continue');await page.waitForURL('**/02_continue_your_work.html*');
  if(!await page.getByText('Compare two studies').count()) throw Error('Work step not restored');
  await screenshot('06-work');await click('hit_stuck');await page.waitForURL('**/03_when_you_are_stuck.html*');
  for(const [name,text] of [['v2_choice_start','Open your notes and choose one sentence'],['v2_choice_small','Write just the first line'],['v2_choice_source','Open the reading list and find one source']]) {
    await click(name);if(!await page.getByText(text,{exact:false}).count()) throw Error('Missing '+name);
  }
  await screenshot('07-stuck');await click('v2_try_suggestion');await page.waitForURL('**/02_continue_your_work.html*');
  if(!await page.getByText('Open the reading list and find one source.',{exact:false}).count()) throw Error('Chosen smaller step not applied');
  await click('hit_pause');await page.waitForURL('**/04_leave_a_thread.html*');
  if(await where.inputValue()!=='Stopped at the literature synthesis') throw Error('Context was not editable on return');
  if(await next.inputValue()!=='Open the reading list and find one source.') throw Error('Updated next step was not editable on return');
  await next.fill('A'.repeat(70));if((await next.inputValue()).length!==48) throw Error('Input limit not enforced');
  await next.fill('Review the first source');await click('hit_save_with_variables');await page.waitForURL('**/05_ready_to_return.html*');
  await click('hit_home');await page.waitForURL('**/page_1.html*');
  if(!await page.getByText('Review the first source').count()) throw Error('Edited action not restored');
  await click('hit_continue');await page.waitForURL('**/02_continue_your_work.html*');await click('v3_finish_step');await page.waitForURL('**/06_step_complete.html*');
  if(!await page.getByText('That step',{exact:false}).count())throw Error('Completion feedback missing');
  await screenshot('08-completed');await click('complete_home');await page.waitForURL('**/page_1.html*');
  if(!await page.getByText('Finished the last step.').count())throw Error('Completion state not reflected');
  return {ok:true,screen:'430x932',validation:'both empty and partial',editAfterReturn:true,maxLength:48,stuckChoices:3,chosenStepCarries:true,finishStep:true};
}
