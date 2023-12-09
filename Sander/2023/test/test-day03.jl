using AdventofCode: day03

@testset "Day 3" begin

    @testset "Day 3, part 1" begin
        testfiles = Dict(
            "input03-test1.txt" => 4361,
        )
        for (file, result) in testfiles
            data = day03.parse_file(joinpath(INPUT, file))
            @test day03.a(data) == result
        end
    end

    @testset "Day 3, part 2" begin
        testfiles = Dict(
            "input03-test1.txt" => 467835,
        )
        for (file, result) in testfiles
            data = day03.parse_file(joinpath(INPUT, file))
            @test day03.b(data) == result
        end
    end

end