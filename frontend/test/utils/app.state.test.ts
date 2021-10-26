import { User } from '../../src/model/user';
import { appState } from '../../src/utils/app.state';

describe('App State', () => {
  it('Should contain user', () => {
    expect(appState.user).toBeNull();
  });

  it('Should set user', () => {
    const user: User = {
      id: 1,
      email: 'Test@test.de',
      firstname: 'Test',
      is_active: true,
      is_superuser: true,
      lastname: 'Test'
    };

    appState.user = user;
    expect(appState.user).toEqual(user);
  });
});
