describe('Tests login workflow', () => {
  it('Home page redirects to login', () => {
    cy.visit('/')
    cy.url().should('include', '/login')
  })

  it('Filling in email and passwords goes to', () => {
    cy.visit('/login')
    cy.get('[data-cy=email]').type(Cypress.env('TEST_USER_EMAIL'))
    cy.get('[data-cy=password]').type(Cypress.env('TEST_USER_PASS'))
    cy.contains('[data-cy=submit]', 'Log In').click()
    cy.url().should('include', '/')
  })
})
