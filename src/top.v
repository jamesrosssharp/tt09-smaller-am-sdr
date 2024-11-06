/* vim: set et ts=4 sw=4: */

/*
	Tiny AM SDR

top.v: Top level

Copyright 2023 J.R.Sharp

*/

module top (
	input	clk,
	input	RSTb,
	output  COMP_OUT,
	output 	reg PWM_OUT,
	input   COMP_IN,

	input 	SCK,
	input	MOSI,
	input	CS

);

wire [19:0] phase_inc;
wire [2:0]  gain_spi;

spi spi0
(
    clk,
    RSTb,
    MOSI,
    SCK,
    CS,

    phase_inc,
    gain_spi

);

wire [7:0] if_out;

rf_mixer_nco nco0
(
    clk,
    RSTb,
    COMP_IN,
    COMP_OUT,
    phase_inc,
    if_out
);

wire [7:0] if_filt_out;

if_filter filt0
(
    clk,
    RSTb,
    if_out,
    if_filt_out,
    gain_spi
);

wire [7:0] env_det_out;

envelope_detector det0
(
    clk,
    RSTb,
    if_filt_out,
    env_det_out
);

reg [7:0] count; 

always @(posedge clk) begin
	if (RSTb == 1'b0) begin
		count <= 8'd0;
		PWM_OUT <= 1'b0;
	end else begin
		count <= count + 1;
		PWM_OUT <= (count < env_det_out) ? 1'b1 : 1'b0;
	end	
end

endmodule
