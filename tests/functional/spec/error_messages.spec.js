import TestErrorsPage from "../generated_pages/error_messages/test-errors.page.js";

describe("Error Messages", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_error_messages.json");
  });

  it("Given a survey has an error when errors are displayed then page error messages are correct", () => {
    $(TestErrorsPage.testNumber()).setValue("cat");
    $(TestErrorsPage.testPercent()).setValue("101");
    $(TestErrorsPage.testCurrency()).setValue("123.456");
    $(TestErrorsPage.submit()).click();
    expect($(TestErrorsPage.errorHeader()).getText()).to.contain("There are 3 problems with your answer");
    expect($(TestErrorsPage.errorNumber(1)).getText()).to.contain("Enter a number");
    expect($(TestErrorsPage.errorNumber(2)).getText()).to.contain("Enter an answer less than or equal to 100");
    expect($(TestErrorsPage.errorNumber(3)).getText()).to.contain("Enter a number rounded to 2 decimal places");
  });

  it("Given a survey has 1 error when error is displayed then error header is displayed correct", () => {
    $(TestErrorsPage.testNumber()).setValue("cat");
    $(TestErrorsPage.testPercent()).setValue("100");
    $(TestErrorsPage.testCurrency()).setValue("123.45");
    $(TestErrorsPage.submit()).click();
    expect($(TestErrorsPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
  });

  it("Given a survey has an error when errors are displayed then answer error messages are correct", () => {
    $(TestErrorsPage.testNumber()).setValue("cat");
    $(TestErrorsPage.testPercent()).setValue("101");
    $(TestErrorsPage.testCurrency()).setValue("123.456");
    $(TestErrorsPage.submit()).click();

    expect($(TestErrorsPage.testNumberErrorItem()).getText()).to.contain("Enter a number");
    expect($(TestErrorsPage.testPercentErrorItem()).getText()).to.contain("Enter an answer less than or equal to 100");
    expect($(TestErrorsPage.testCurrencyErrorItem()).getText()).to.contain("Enter a number rounded to 2 decimal places");
  });

  it("Given a survey has an error when errors message is clicked then the correct answer is focused", () => {
    $(TestErrorsPage.testNumber()).setValue("cat");
    $(TestErrorsPage.testPercent()).setValue("101");
    $(TestErrorsPage.testCurrency()).setValue("123.456");
    $(TestErrorsPage.submit()).click();

    $(TestErrorsPage.errorNumber(2)).click();
    expect($(TestErrorsPage.testPercent()).isFocused()).to.be.true;
    $(TestErrorsPage.errorNumber(3)).click();
    expect($(TestErrorsPage.testCurrency()).isFocused()).to.be.true;
    $(TestErrorsPage.errorNumber(1)).click();
    expect($(TestErrorsPage.testNumber()).isFocused()).to.be.true;
  });
});
