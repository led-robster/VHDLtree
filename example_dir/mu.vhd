

entity mu is
    port (
        clk   : in std_logic;
        reset : in std_logic;
        
    );
end entity mu;

architecture rtl of mu is

begin

    i_mv : entity lib.mv(rtl)
    generic map (
        
    )
    port map (
        
    );

end architecture;