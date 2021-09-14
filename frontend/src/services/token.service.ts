export class TokenService {
  private static TOKEN_KEY: string = 'access_token';
  private static REFRESH_TOKEN_KEY: string = 'refresh_token';

  /**
   * Returns the current stored token
   *
   * @returns The token
   */
  public static getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Stores the given token in the local storage
   *
   * @param accessToken The token to be stored
   */
  public static saveToken(accessToken: string): void {
    localStorage.setItem(this.TOKEN_KEY, accessToken);
  }

  /**
   * Removes the current token
   */
  public static removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  /**
   * Returns the current stored refresh token
   *
   * @returns The refresh token
   */
  public static getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  /**
   * Stores the given refresh token in the local storage
   *
   * @param refreshToken The refresh token to be stored
   */
  public static saveRefreshToken(refreshToken: string): void {
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
  }

  /**
   * Removes the stored refresh token
   */
  public static removeRefreshToken(): void {
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
  }
}
