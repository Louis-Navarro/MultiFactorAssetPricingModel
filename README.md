# Multi Factor Capital Asset Pricing Modelling (MF-CAPM)

## Table of Contents## Introduction

1. [Introduction](#introduction)
2. [Price Modelling](#price-modelling)
   - [Traditional CAPM](#traditional-capm)
   - [CAPM With Alpha](#capm-with-alpha)
   - [Multi Factor Capital Asset Pricing Modelling](#multi-factor-capital-asset-pricing-modelling)
3. [Experiment](#experiment)
4. [Results](#results)

In this repository, we explore an extension of the Capital Asset Price Model (CAPM) that link the returns of an asset to multiple factors.

The motivation behind this is to explore how movement in multiple distinct and diverse markets affect the price of an asset. For example, if we consider a material mining company, the price of its stock may have a relatively low beta relative to the US Market or the Total Stock Market, but a high beta relative to the Commodities Market or Emerging Markets.

## Price Modelling

### Traditional CAPM

The typical CAPM model assumes the expected return of an asset is dependent on the risk free rate of return $r_f$, and the asset's sensitivity to systematic risk, i.e. its sensitivity $\beta_i$ to the market return $r_m$. The expected rate of return for asset $i$ is given by:

$$E[r_i] = E[r_f] + \beta_i(E[r_m]-E[r_f])$$

Intuitively, the return of asset $i$ cumulates the risk free return, with the market risk premium, the coefficient $\beta$ adjusts the market premium to how sensitive and volatile the asset is to market movement.

### CAPM With Alpha

A common extension to the CAPM is incorperating a coefficient, $\alpha$, called **Jensen's alpha**, to represent the realised returns of the asset that aren't explained by the market movement and the traditional CAPM model (the **edge** on the market).

We define Jensen's alpha by:

$$\alpha_i = r_i - r_f - \beta_i(r_m-r_f)$$

Note: Here we do not use expected returns but instead realised returns. Jensen's alpha essentially addresses CAPM limitation to predicting a asset's return.

We can also write the equation as:

$$r_i - r_f = \alpha_i + \beta_i(r_m-r_f)$$

### Multi Factor Capital Asset Pricing Modelling

Until now, we've been working under the assumption that there is a single "market return" and a single systematic risk. While this should be true is theory (by definition of the systematic risk), in reality assets can usually be clustered into different markets or sectors (e.g. technology, commodities, retail, etc.) each of which could have its own expected market return and systematic risk.

For example, a change in price of energy commodities, such as oil, may largely affect energy companies such as Exxon and Vistra, but may not have any effect on technology companies such as Apple and Microsoft.

Therefore, we use 3 benchmark markets:

- US Market (\$SPY): $r_u$
- Commodities Market (\$DBC): $r_c$
- Emerging Market (\$EEM): $r_e$

We hypothesise that the asset's return is related to the risk free rate, each of the market returns, and the asset's unexplained returns. Thus we model the return of an asset with:

$$r =  r_f + \alpha + \beta_u(r_u-r_f) + \beta_c(r_c-r_f) + \beta_e(r_e-r_f)$$

We can generalise this formula to use $n$ markets, with returns $r_{m,1}, r_{m,2}, ..., r_{m,n}$, and asset's sensitivity to the markets $\beta_1, \beta_2, ..., \beta_n$:

$$r =  r_f + \alpha + \sum\limits_{i=1}^n{\beta_i(r_{m,i}-r_f)}$$

## Experiment

We collect the monthly Open-High-Low-Close data for the tickers through AlphaVantage. We then calculate the monthly percente change of the Close prices, yielding the monthly returns for both the asset and the markets.

We also download the 3 Months US Treasury Bills from AlphaVantage, scale to obtain the monthly rate of return, and use that as the risk free rate.

We estimate the coefficient by using Ordinary Least Squares regression on the following equation, using the realised asset and market returns, and the real risk free rate:

$$r - r_f = \alpha + \beta_u(r_u-r_f) + \beta_c(r_c-r_f) + \beta_e(r_e-r_f) + \varepsilon$$

We also calculate the the simple CAPM, with Jensen's alpha, with OLS to solve the follow equation:

$$r - r_f = \alpha' + \beta_u'(r_u-r_f) + \varepsilon$$

We then compare the coefficients $\beta_u$ and $\beta_u'$, look for non-trivial $\beta_c$ and $\beta_e$, and look for an improvement in the $R^2$ value of the models.

## Results

Results pending as I perform the analysis for many stocks in different sectors.
